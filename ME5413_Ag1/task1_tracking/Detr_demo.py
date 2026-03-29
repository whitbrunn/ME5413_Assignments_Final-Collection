from AIDetector_pytorch import Detector
import imutils
import cv2
import glob
import os
from PIL import Image



def IOU_succ(bbox1, bbox2):
    bx0, by0, bxr, byr = bbox1
    gx0, gy0, gxr,gyr = bbox2
    
    xmin = max(bx0, gx0)
    ymin = max(by0, gy0)

    xmax = min(bxr, gxr)
    ymax = min(byr, gyr)

    IOU_w = max(0, xmax-xmin)
    IOU_h = max(0, ymax-ymin)

    IOU_a = IOU_w * IOU_h

    b1_a = (bbox1[2]-bbox1[0]) * (bbox1[3]-bbox1[1])
    b2_a = (bbox2[2]-bbox2[0]) * (bbox2[3]-bbox2[1])
    succ = IOU_a/(b1_a+b2_a-IOU_a)

    return succ


def main():
    
    name = 'demo'

    det = Detector()

    seq_id = 3
    seq_path = f"data/seq{str(seq_id)}"
    track_id_lst = [1,1, (1, 47),4,1]
    
    

    img_path_lst = sorted(glob.glob(os.path.join(seq_path, "img", "*.jpg")))

    fps = 2
    t = len(img_path_lst)/fps

    size = None
    videoWriter = None
    ct=0


    # Store file
    save_path = f"results/2_objectdetection_withassociation/trackresults_ODA_seq{seq_id}.txt"
    if os.path.exists(save_path):
        os.remove(save_path)
        print(f"Update {save_path}.")
    save_f = open(save_path,"a",encoding="utf-8")

    for img_path in img_path_lst:
        ct+=1
        im = Image.open(img_path)
        if im is None:
            break
        
        result = det.feedCap(im)
        bbox_info = result['bbox_dic']
        # print(bbox_info)

        track_id = track_id_lst[seq_id-1]

        m = ""
        flag = 0
        if bbox_info != {}:
            if type(track_id) != type((2,3)):
                if str(track_id) in bbox_info:
                    flag = 1
            else:
                m = "m"
                id0 = track_id[0]
                id1 = track_id[1]
                track_id = id0
                if str(id0) in bbox_info:
                    flag = 1
                
                if str(id1) in bbox_info:
                    flag = 1
                    track_id = id1
                
                
        if flag:
            tar_bbox = bbox_info[str(track_id)]
            bbox_in_xywh = (tar_bbox[0], tar_bbox[1], tar_bbox[2]-tar_bbox[0],tar_bbox[3]-tar_bbox[1])
            print(f"{ct}{m}, ID-{track_id} BBox in (x,y,width,height): {bbox_in_xywh}")
            save_f.write(str(bbox_in_xywh).strip("()").replace(" ","")+"\n")
        else:
            print(f"{ct}{m}, No ID-{track_id} BBox info so far!")
            save_f.write("NaN\n")
        
        
        result = result['frame']
        result = imutils.resize(result, height=500)
        
        

        # if videoWriter is None:
        #     fourcc = cv2.VideoWriter_fourcc(
        #         'm', 'p', '4', 'v')  # opencv3.0
        #     videoWriter = cv2.VideoWriter(
        #         'result.mp4', fourcc, fps, (result.shape[1], result.shape[0]))

        

        # videoWriter.write(result)
        cv2.imshow(name, result)
        # k = cv2.waitKey(0)
        k = cv2.waitKey(1) & 0xff
        if k==ord('q'):
            break
        # if cv2.getWindowProperty(name, cv2.WND_PROP_AUTOSIZE) < 1:
        #     # 点x退出
        #     break
        # except Exception as e:
        #     print(e)
        #     break

    save_f.close()
    # videoWriter.release()
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    
    main()