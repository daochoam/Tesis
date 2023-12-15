import numpy as np
import fnmatch
import yaml
import cv2
import glob
import os


def load_and_resize_image(file_path, scale_percent=100):
    img = cv2.imread(file_path)

    # Obtener las dimensiones originales de la imagen
    height, width = img.shape[:2]

    # Calcular el porcentaje de escala
    scale_factor = scale_percent / 100.0

    # Calcular las nuevas dimensiones
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Redimensionar la imagen manteniendo la proporcionalidad
    img_resized = cv2.resize(img, (new_width, new_height))

    return img_resized


class Calibrate_Camera:

    def Read_CameraP(self, C_Parameters):
        with open(C_Parameters) as f:
            loadeddict = yaml.load(f, Loader=yaml.SafeLoader)
            CamMatrix = np.array(loadeddict.get('Camera_Matrix'))
            Dist_Coeffs = np.array(loadeddict.get('Distortion_Coefficients'))
        return CamMatrix, Dist_Coeffs

    def Undistor(self, img, Camera_Matrix, Dist_Coeffs):
        h,  w = img.shape[:2]
        NewCam_Matrix, ROI = cv2.getOptimalNewCameraMatrix(
            Camera_Matrix, Dist_Coeffs, (w, h), 1, (w, h))
        mapx, mapy = cv2.initUndistortRectifyMap(
            Camera_Matrix, Dist_Coeffs, None, NewCam_Matrix, (w, h), 5)
        Dist = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        x, y, w, h = ROI
        Dist = Dist[y:y+h, x:x+w]
        return Dist

    def Camera_Calibrate(self, C_Parameters="Camera_Parameter.yaml", patternsize=[9, 6]):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        patternsize = [9, 6]

        # preparar puntos de objeto, como (0,0,0), (1,0,0), (2,0,0) ...., (6,5,0)
        objp = np.zeros((patternsize[0]*patternsize[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:patternsize[0],
                               0:patternsize[1]].T.reshape(-1, 2)
        # Arreglos para almacenar puntos de objetos y puntos de imagen de todas las imágenes.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.

        # images = glob.glob("ChessBoard/*.jpg")
        # Patrón para las extensiones deseadas
        image_extensions = ['*.jpg', '*.JPG',
                            '*.JPEG', '*.jpeg', '*.PNG', '*.png']

        # Utilizar fnmatch.filter para encontrar archivos que coincidan con el patrón
        images = sorted([file for ext in image_extensions for file in glob.glob(
            'ChessBoard/' + ext)], key=os.path.basename)

        print(images)
        i = 0
        for fname in images:
            img = load_and_resize_image(fname, 100)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, patternsize, None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(
                    img, patternsize, corners2, ret)
                # cv2.waitKey(50)
                i = i+1

        cv2.destroyAllWindows()
        RMS, Camera_Matrix, Dist_Coeffs, Rotation_V, Translation_V = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None)

        mean_error = 0
        tot_error = 0
        for i in range(len(objpoints)):
            imgpoints2, _ = cv2.projectPoints(
                objpoints[i], Rotation_V[i], Translation_V[i], Camera_Matrix, Dist_Coeffs)
            error = cv2.norm(imgpoints[i], imgpoints2,
                             cv2.NORM_L2)/len(imgpoints2)
            tot_error += error

        i = 0
        for fname in images:
            img = cv2.imread(fname)
            Dist = self.Undistor(img, Camera_Matrix, Dist_Coeffs)
            # cv2.waitKey(50)
            i = i+1

        data = {'Calibrate_Accuracy': np.asarray(RMS).tolist(), 'Camera_Matrix': np.asarray(Camera_Matrix).tolist(), 'Distortion_Coefficients': np.asarray(Dist_Coeffs).tolist(),
                'Rotation_Vector': np.asarray(Rotation_V).tolist(), 'Translation_V': np.asarray(Translation_V).tolist()}
        with open(C_Parameters, "w") as f:
            yaml.dump(data, f)
