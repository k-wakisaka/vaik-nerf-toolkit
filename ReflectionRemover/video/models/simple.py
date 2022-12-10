import tensorflow as tf


def prepare(input_shape):
    input = tf.keras.Input(input_shape)

    x = tf.keras.layers.Conv3D(16, (3, 3, 3), activation='relu', padding='same')(input)
    x = tf.keras.layers.MaxPooling3D((1, 2, 2), padding='same')(x)
    x = tf.keras.layers.Conv3D(8, (3, 3, 3), activation='relu', padding='same')(x)
    x = tf.keras.layers.MaxPooling3D((1, 2, 2), padding='same')(x)
    x = tf.keras.layers.Conv3D(4, (3, 3, 3), activation='relu', padding='same')(x)
    encoded = tf.keras.layers.MaxPooling3D((1, 2, 2), padding='same', name='encoder')(x)

    x = tf.keras.layers.Conv3D(4, (3, 3, 3), activation='relu', padding='same')(encoded)
    x = tf.keras.layers.UpSampling3D((1, 2, 2))(x)
    x = tf.keras.layers.Conv3D(8, (3, 3, 3), activation='relu', padding='same')(x)
    x = tf.keras.layers.UpSampling3D((1, 2, 2))(x)
    x = tf.keras.layers.Conv3D(16, (3, 3, 3), activation='relu', padding='same')(x)
    x = tf.keras.layers.UpSampling3D((1, 2, 2))(x)
    decoded = tf.keras.layers.Conv3D(3, (3, 3, 3), activation='sigmoid', padding='same')(x)

    autoencoder = tf.keras.Model(input, decoded)
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
    return autoencoder
