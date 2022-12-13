import tensorflow as tf
import tensorflow_addons as tfa

def conv2d_block(input, num_filters):
    x = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(num_filters, 3, padding="same"))(input)
    x = tf.keras.layers.GroupNormalization()(x)
    x = tf.keras.layers.Activation("swish")(x)

    x = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(num_filters, 3, padding="same"))(x)
    x = tf.keras.layers.GroupNormalization()(x)
    x = tf.keras.layers.Activation("swish")(x)
    return x

def conv3d_identify_block(input, num_filters, dilate, kernel=3):
    x = tf.keras.layers.Conv3D(num_filters, kernel, dilation_rate=(dilate, 1, 1), activation="swish", padding="same")(input)
    x = tf.keras.layers.GroupNormalization()(x)
    return x

def conv3d_convolution_block(input, num_filters, dilate, kernel=3):
    x = tf.keras.layers.Conv3D(num_filters, kernel, dilation_rate=(dilate, 1, 1), activation="swish", padding="same")(input)
    x = tf.keras.layers.GroupNormalization()(x)
    return x

def conv3d_convolution_trans_block(input, num_filters, dilate, kernel=3):
    x = tf.keras.layers.Conv3DTranspose(num_filters, kernel, dilation_rate=(dilate, 1, 1), activation="swish", padding="same")(input)
    x = tf.keras.layers.GroupNormalization()(x)
    return x

def conv3d_convolution_stride_block(input, num_filters, dilate):
    x = tf.keras.layers.Conv3D(num_filters, 3, dilation_rate=(dilate, 1, 1), strides=(1, 2, 2), activation="swish", padding="same")(input)
    x = tf.keras.layers.GroupNormalization()(x)
    x = tf.keras.layers.Conv3D(num_filters, 3, dilation_rate=(dilate, 1, 1), padding="same")(x)
    input = tf.keras.layers.Conv3D(num_filters, 1, strides=(1, 2, 2), padding="same")(input)
    x = tf.keras.layers.Add()([input, x])
    x = tf.keras.layers.Activation("swish")(x)
    x = tf.keras.layers.GroupNormalization()(x)
    return x

def tcn_identify_block(input, num_filters):
    tmp_num_filters = max(32, num_filters//2)
    x1 = conv3d_identify_block(input, tmp_num_filters, 1, 1)
    x2 = conv3d_identify_block(input, tmp_num_filters, 1)
    x3 = conv3d_identify_block(input, tmp_num_filters, 2)
    x4 = conv3d_identify_block(input, tmp_num_filters, 4)
    x5 = tf.keras.layers.Concatenate()([x1, x2, x3, x4])
    p = tf.keras.layers.Conv3D(num_filters, 3, activation="swish", padding="same")(x5)
    p = tf.keras.layers.GroupNormalization()(p)
    return p

def tcn_convolution_block(input, num_filters):
    tmp_num_filters = max(32, num_filters//2)
    x1 = conv3d_convolution_block(input, tmp_num_filters, 1, 1)
    x2 = conv3d_convolution_block(input, tmp_num_filters, 1)
    x3 = conv3d_convolution_block(input, tmp_num_filters, 2)
    x4 = conv3d_convolution_block(input, tmp_num_filters, 4)
    x5 = tf.keras.layers.Concatenate()([x1, x2, x3, x4])
    p = tf.keras.layers.Conv3D(num_filters, 3, strides=(1, 2, 2), activation="swish", padding="same")(x5)
    p = tf.keras.layers.GroupNormalization()(p)
    return x5, p


def tcn_convolution_block_no_stride(input, num_filters):
    tmp_num_filters = max(32, num_filters//2)
    x1 = conv3d_convolution_block(input, tmp_num_filters, 1, 1)
    x2 = conv3d_convolution_block(input, tmp_num_filters, 1)
    x3 = conv3d_convolution_block(input, tmp_num_filters, 2)
    x4 = conv3d_convolution_block(input, tmp_num_filters, 4)
    x5 = tf.keras.layers.Concatenate()([x1, x2, x3, x4])
    p = tf.keras.layers.Conv3D(num_filters, 3, activation="swish", padding="same")(x5)
    p = tf.keras.layers.GroupNormalization()(p)
    return p

def tcn_convolution_stride_block(input, num_filters):
    tmp_num_filters = max(32, num_filters//2)
    x1 = conv3d_convolution_block(input, tmp_num_filters, 1, 1)
    x2 = conv3d_convolution_block(input, tmp_num_filters, 1)
    x3 = conv3d_convolution_block(input, tmp_num_filters, 2)
    x4 = conv3d_convolution_block(input, tmp_num_filters, 4)
    x5 = tf.keras.layers.Concatenate()([x1, x2, x3, x4])
    p = tf.keras.layers.Conv3D(num_filters, 3, strides=(1, 2, 2), activation="swish", padding="same")(x5)
    p = tf.keras.layers.GroupNormalization()(p)
    return x5, p

def encoder2d_block(input, num_filters):
    x = conv2d_block(input, num_filters)
    p = tf.keras.layers.TimeDistributed(tf.keras.layers.MaxPool2D((2, 2)))(x)
    return x, p

def encodertcn_block(input, num_filters):
    x, p = tcn_convolution_stride_block(input, num_filters)
    return x, p

def decoder2d_block(input, skip_features, num_filters):
    x = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2DTranspose(num_filters, (2, 2), strides=(2, 2), padding="same"))(input)
    x = tf.keras.layers.TimeDistributed(tf.keras.layers.Concatenate())([x, skip_features])
    x = conv2d_block(x, num_filters)
    return x

def decodertcn_block(input, skip_features, num_filters):
    x = tf.keras.layers.Conv3DTranspose(num_filters, 3, strides=(1, 2, 2), padding="same")(input)
    x = tf.keras.layers.Concatenate()([x, skip_features])
    x = tcn_convolution_block_no_stride(x, num_filters)
    return x

def prepare(input_shape, base_dim=32):
    inputs = tf.keras.layers.Input(input_shape)

    s1, p1 = encoder2d_block(inputs, base_dim)
    s2, p2 = encodertcn_block(p1, base_dim*2)
    s3, p3 = encodertcn_block(p2, base_dim*4)
    s4, p4 = encodertcn_block(p3, base_dim*8)

    b0 = tcn_identify_block(p4, base_dim*8)

    d1 = decodertcn_block(b0, s4, base_dim*8)
    d2 = decodertcn_block(d1, s3, base_dim*4)
    d3 = decodertcn_block(d2, s2, base_dim*2)
    d4 = decoder2d_block(d3, s1, base_dim)

    outputs = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(3, 1, padding="same", activation="sigmoid"))(d4)

    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='mse')
    return model
