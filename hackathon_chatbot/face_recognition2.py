import cv2
import face_recognition

def find_face_encodings(image_path):
    # reading image
    image = cv2.imread(image_path)    # get face encodings from the image
    face_enc = face_recognition.face_encodings(image)    # return face encodings
    return face_enc[0]

def compare_faces(img_1_path, img_2_path):

    image_1 = find_face_encodings(img_1_path)
    image_2 = find_face_encodings(img_2_path)



    # checking both images are same
    is_same = face_recognition.compare_faces([image_1], image_2)[0]
    print(f"Is Same: {is_same}")
    if is_same:
        # finding the distance level between images
        distance = face_recognition.face_distance([image_1], image_2)
        distance = round(distance[0] * 100)
        
        # calcuating accuracy level between images
        accuracy = 100 - round(distance)    
        print("The images are same")
        print(f"Accuracy Level: {accuracy}%")
        return True
    else:
        print("The images are not same")
        return False