import tensorflow as tf
import math
#classification
# 추출한 skeleton landmarks 좌표 x,y,z 값을 input으로 활용
inputs = tf.keras.layers.Input(shape=(99))
layer = tf.keras.layers.Dense(64, activation='relu')(inputs)
layer = tf.keras.layers.Dense(32, activation='relu')(layer)
output = tf.keras.layers.Dense(4, activation='softmax')(layer)
model = tf.keras.models.Model(inputs, output)
model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])
model.summary

# 앵글 계산 함수
def calculateAngle(landmark1, landmark2, landmark3):

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360
    
    # Return the calculated angle.
    return angle
    
# 함수 실행
# Calculate the angle between the three landmarks.
angle = calculateAngle((558, 326, 0), (642, 333, 0), (718, 321, 0))

# Display the calculated angle.
print(f'The calculated angle is {angle}')