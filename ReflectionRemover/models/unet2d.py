import tensorflow as tf

def conv2d_block(input, num_filters):
    x = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(num_filters, 3, padding="same"))(input)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)

    x = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(num_filters, 3, padding="same"))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)
    return x

def conv3d_resblock(input, num_filters, dilate):
    x = tf.keras.layers.Conv3D(num_filters, 3, dilation_rate=(dilate, 1, 1), activation="relu", padding="same")(input)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv3D(num_filters, 3, dilation_rate=(dilate, 1, 1), padding="same")(x)
    x = tf.keras.layers.Add()([input, x])
    x = tf.keras.layers.ReLU()(x)
    x = tf.keras.layers.BatchNormalization()(x)
    return x

def encoder2d_block(input, num_filters):
    x = conv2d_block(input, num_filters)
    p = tf.keras.layers.TimeDistributed(tf.keras.layers.MaxPool2D((2, 2)))(x)
    return x, p

def decoder2d_block(input, skip_features, num_filters):
    x = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2DTranspose(num_filters, (2, 2), strides=(2, 2), padding="same"))(input)
    x = tf.keras.layers.TimeDistributed(tf.keras.layers.Concatenate())([x, skip_features])
    x = conv2d_block(x, num_filters)
    return x

def prepare(input_shape, base_dim=8):
    inputs = tf.keras.layers.Input(input_shape)

    s1, p1 = encoder2d_block(inputs, base_dim)
    s2, p2 = encoder2d_block(p1, base_dim*2)
    s3, p3 = encoder2d_block(p2, base_dim*4)
    s4, p4 = encoder2d_block(p3, base_dim*8)

    b0 = conv3d_resblock(p4, base_dim*8, 1)
    b1 = conv3d_resblock(b0, base_dim*8, 2)
    b2 = conv3d_resblock(b1, base_dim*8, 3)
    b3 = conv3d_resblock(b2, base_dim*8, 4)

    d1 = decoder2d_block(b3, s4, base_dim*8)
    d2 = decoder2d_block(d1, s3, base_dim*4)
    d3 = decoder2d_block(d2, s2, base_dim*2)
    d4 = decoder2d_block(d3, s1, base_dim)

    outputs = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(3, 1, padding="same", activation="sigmoid"))(d4)

    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model
