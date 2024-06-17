from ultralytics import YOLO
# model = YOLO('yolov8n.pt')



def image_detection(path,model):
    print('detection')
    model = YOLO(f'models/{model}.pt')
    print('detection2')

    results = model(path,imgsz=640)
    for idx, result in enumerate(results):

        regions = []

        for i, box in enumerate(result.boxes.xyxy.tolist()):
            class_index = int(result.boxes.cls[i])
            # Utiliser l'attribut 'names' pour obtenir le nom de l'objet détecté
            print(" avant")
            print(" results",result.names[class_index])
            print(" apres")
            object_name=result.names[class_index]
            # Convert normalized coordinates to absolute pixel values
            x_abs = int(box[0])
            y_abs = int(box[1])
            width_abs = int((box[2] - box[0]))
            height_abs = int((box[3] - box[1]))

            shape_attributes = {
                'name': 'rect',
                'x': x_abs,
                'y': y_abs,
                'width': width_abs,
                'height': height_abs
            }


            regions.append({
                'shape_attributes': shape_attributes,
                'region_attributes':{"objet": object_name,},
            })


        annotations = {
            'liste_objet':result.names,
            'regions': regions,
            'file_attributes': 'file_attributes'
        }
    print('annotations= ',annotations)
    return annotations
