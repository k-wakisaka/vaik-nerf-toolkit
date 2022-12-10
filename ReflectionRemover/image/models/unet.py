import tensorflow as tf
import tensorflow_addons as tfa

def conv_block(input, num_filters):
    x = tf.keras.layers.Conv2D(num_filters, 3, padding="same")(input)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("swish")(x)

    x = tf.keras.layers.Conv2D(num_filters, 3, padding="same")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("swish")(x)

    return x

def encoder_block(input, num_filters):
    x = conv_block(input, num_filters)
    p = tf.keras.layers.MaxPool2D((2, 2))(x)
    return x, p

def decoder_block(input, skip_features, num_filters):
    x = tf.keras.layers.Conv2DTranspose(num_filters, (2, 2), strides=(2, 2), padding="same")(input)
    x = tf.keras.layers.Concatenate()([x, skip_features])
    x = conv_block(x, num_filters)
    return x

def prepare(input_shape, base_dim=64):
    inputs = tf.keras.layers.Input(input_shape)

    s1, p1 = encoder_block(inputs, base_dim)
    s2, p2 = encoder_block(p1, base_dim*2)
    s3, p3 = encoder_block(p2, base_dim*4)
    s4, p4 = encoder_block(p3, base_dim*8)

    b1 = conv_block(p4, base_dim*16)

    d1 = decoder_block(b1, s4, base_dim*8)
    d2 = decoder_block(d1, s3, base_dim*4)
    d3 = decoder_block(d2, s2, base_dim*2)
    d4 = decoder_block(d3, s1, base_dim)

    outputs = tf.keras.layers.Conv2D(3, 1, padding="same", activation="sigmoid")(d4)

    model = tf.keras.Model(inputs, outputs)

    model.compile(optimizer='adam', loss=tfa.losses.SigmoidFocalCrossEntropy())
    return model
