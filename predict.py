import tensorflow as tf
import numpy as np



model = tf.keras.models.load_model("models/traffic_sign_model_final.keras")



class_names = [
    "20 km/h Speed Limit",
    "30 km/h Speed Limit",
    "50 km/h Speed Limit",
    "60 km/h Speed Limit",
    "70 km/h Speed Limit",
    "80 km/h Speed Limit",
    "End 80 km/h",
    "100 km/h Speed Limit",
    "120 km/h Speed Limit",
    "No Passing",
    "No Passing (Trucks)",
    "Road Intersection",
    "Priority Road",
    "Yield",
    "STOP",
    "No Vehicles",
    "No Trucks",
    "No Entry",
    "General Warning",
    "Left Curve",
    "Right Curve",
    "Double Curve",
    "Bumpy Road",
    "Slippery Road",
    "Road Narrows",
    "Road Work",
    "Traffic Signals",
    "Pedestrians",
    "Children Crossing",
    "Bicycles Crossing",
    "Snow / Ice",
    "Wild Animals",
    "End Speed Limit",
    "Turn Right",
    "Turn Left",
    "Go Straight",
    "Straight or Right",
    "Straight or Left",
    "Keep Right",
    "Keep Left",
    "Roundabout",
    "End No Passing",
    "End No Passing Trucks"
]



traffic_info = {

    "STOP": {
        "risk": "🔴 HIGH",
        "action": "Stop your vehicle completely before moving.",
        "rule": "Proceed only when the road is clear."
    },

    "Yield": {
        "risk": "🟠 MEDIUM",
        "action": "Slow down and give priority to other vehicles.",
        "rule": "Do not stop unless necessary."
    },

    "No Entry": {
        "risk": "🔴 HIGH",
        "action": "Do not enter this road.",
        "rule": "Entering is prohibited."
    },

    "Turn Left": {
        "risk": "🟡 LOW",
        "action": "Turn left safely.",
        "rule": "Follow the mandatory direction."
    },

    "Turn Right": {
        "risk": "🟡 LOW",
        "action": "Turn right safely.",
        "rule": "Follow the mandatory direction."
    }

}



def predict_image(image):

    image = image.resize((32, 32))

    image = np.array(image)

    image = image / 255.0

    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image, verbose=0)

    predicted_class = np.argmax(prediction)

    confidence = float(np.max(prediction) * 100)

    print("="*50)
    print("Predicted Index :", predicted_class)
    print("Predicted Sign  :", class_names[predicted_class])
    print("Confidence      :", confidence)

    top5 = np.argsort(prediction[0])[::-1][:5]

    print("\nTop 5 Predictions")

    for i in top5:
        print(i, class_names[i], prediction[0][i])
    print("="*50)

    

    if confidence < 95:

        return {
            "sign": "No Traffic Sign Detected",
            "confidence": confidence,
            "risk": "⚪ NONE",
            "action": "Please point the camera toward a clear traffic sign.",
            "rule": "No traffic rule available."
        }

    sign = class_names[predicted_class]

   

    risk = "🟢 LOW"
    action = "Follow the traffic sign."
    rule = "Drive safely."

    # Speed Limit Signs

    if "Speed Limit" in sign:

        speed = sign.replace("Speed Limit", "").strip()

        action = f"Maintain your speed below {speed}."

        rule = "Follow the posted speed limit."

    

    if sign in traffic_info:

        risk = traffic_info[sign]["risk"]
        action = traffic_info[sign]["action"]
        rule = traffic_info[sign]["rule"]

    return {

        "sign": sign,
        "confidence": confidence,
        "risk": risk,
        "action": action,
        "rule": rule

    }