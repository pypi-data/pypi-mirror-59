import os
import tensorflow as tf
from tensorflow.python.keras.layers import (
    Embedding,
    Bidirectional,
    LSTM,
    BatchNormalization,
)
from tensorflow.python.keras.models import Sequential
import kashgari

from ioflow.configure import read_configure
from ioflow.corpus import get_corpus_processor
from ner_keras.input import generate_tagset, Lookuper, index_table_from_file
from ner_keras.utils import create_dir_if_needed, create_file_dir_if_needed
from tokenizer_tools.tagset.converter.offset_to_biluo import offset_to_biluo
from tf_attention_layer.layers.global_attentioin_layer import GlobalAttentionLayer
from tf_crf_layer.layer import CRF
from tf_crf_layer.loss import ConditionalRandomFieldLoss
from tf_crf_layer.metrics import (
    crf_accuracy,
    SequenceCorrectness,
    sequence_span_accuracy,
)

# Select NVIDIA Graphics
# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '0'

config = read_configure()  # ioflow
corpus = get_corpus_processor(config)
corpus.prepare()  # ?
train_data_generator_func = corpus.get_generator_func(corpus.TRAIN)
eval_data_generator_func = corpus.get_generator_func(corpus.EVAL)

corpus_meta_data = corpus.get_meta_info()
tags_data = generate_tagset(corpus_meta_data["tags"])  # process entity into BIO

train_data = list(train_data_generator_func())
eval_data = list(eval_data_generator_func())

tag_lookuper = Lookuper({v: i for i, v in enumerate(tags_data)})  # tag index
vocab_data_file = config.get("vocabulary_file")
vocabulary_lookuper = index_table_from_file(vocab_data_file)    # dict index

def preprocss(data, maxlen):
    raw_x = []
    raw_y = []

    for offset_data in data:
        tags = offset_to_biluo(offset_data)
        words = offset_data.text

        tag_ids = [tag_lookuper.lookup(i) for i in tags]
        word_ids = [vocabulary_lookuper.lookup(i) for i in words]

        raw_x.append(word_ids)
        raw_y.append(tag_ids)

    if maxlen is None:
        maxlen = max(len(s) for s in raw_x)

    print(">>> maxlen: {}".format(maxlen))

    x = tf.keras.preprocessing.sequence.pad_sequences(
        raw_x, maxlen, padding="post"
    )  # right padding

    # lef padded with -1. Indeed, any integer works as it will be masked
    # y_pos = pad_sequences(y_pos, maxlen, value=-1)
    # y_chunk = pad_sequences(y_chunk, maxlen, value=-1)
    y = tf.keras.preprocessing.sequence.pad_sequences(
        raw_y, maxlen, value=0, padding="post"
    )

    return x, y

MAX_SENTENCE_LEN = config.get("max_sentence_len", 25)

train_x, train_y = preprocss(train_data, MAX_SENTENCE_LEN)
test_x, test_y = preprocss(eval_data, MAX_SENTENCE_LEN)

EPOCHS = config["epochs"]
EMBED_DIM = config["embedding_dim"]
USE_ATTENTION_LAYER = config.get("use_attention_layer", False)
BiLSTM_STACK_CONFIG = config.get("bilstm_stack_config", [])
BATCH_NORMALIZATION_AFTER_EMBEDDING_CONFIG = config.get(
    "use_batch_normalization_after_embedding", False
)
BATCH_NORMALIZATION_AFTER_BILSTM_CONFIG = config.get(
    "use_batch_normalization_after_bilstm", False
)
CRF_PARAMS = config.get("crf_params", {})

vacab_size = vocabulary_lookuper.size()
tag_size = tag_lookuper.size()

# create Bare embedding
# from kashgari.embeddings import BareEmbedding
#
# bare_embed = BareEmbedding(task=kashgari.LABELING,
#                            embedding_size=300)

# create BERT embedding
from kashgari.embeddings import BERTEmbedding

BERT_PATH = './models/bert_base_models/chinese_L-12_H-768_A-12/'
bert_embed = BERTEmbedding(BERT_PATH,
                           task=kashgari.LABELING,
                           sequence_length=100)

model = Sequential()

model.add(bert_embed)
# model.add(
#     Embedding(vacab_size, EMBED_DIM, embeddings_initializer='glorot_normal',
#               mask_zero=True, input_length=MAX_SENTENCE_LEN)
# )

if BATCH_NORMALIZATION_AFTER_EMBEDDING_CONFIG:
    model.add(BatchNormalization())

for bilstm_config in BiLSTM_STACK_CONFIG:
    model.add(Bidirectional(LSTM(return_sequences=True, **bilstm_config)))

if BATCH_NORMALIZATION_AFTER_BILSTM_CONFIG:
    model.add(BatchNormalization())

if USE_ATTENTION_LAYER:
    model.add(GlobalAttentionLayer())

model.add(CRF(tag_size, name="crf", **CRF_PARAMS))

# print model summary
model.summary()

callbacks_list = []

tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=create_dir_if_needed(config["summary_log_dir"])
)
callbacks_list.append(tensorboard_callback)

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    os.path.join(create_dir_if_needed(config["model_dir"]), "cp-{epoch:04d}.ckpt"),
    load_weights_on_restart=True,
    verbose=1,
)
callbacks_list.append(checkpoint_callback)

metrics_list = []

metrics_list.append(crf_accuracy)
metrics_list.append(SequenceCorrectness())
metrics_list.append(sequence_span_accuracy)

loss_func = ConditionalRandomFieldLoss()
# loss_func = crf_loss

model.compile("adam", loss={"crf": loss_func}, metrics=metrics_list)
# model.compile("nadam", loss={"crf": loss_func}, metrics=metrics_list)
model.fit(
    train_x,
    train_y,
    epochs=EPOCHS,
    validation_data=[test_x, test_y],
    callbacks=callbacks_list,
)

# Save the model
model.save(create_file_dir_if_needed(config["h5_model_file"]))

tf.keras.experimental.export_saved_model(
    model, create_dir_if_needed(config["saved_model_dir"]))
