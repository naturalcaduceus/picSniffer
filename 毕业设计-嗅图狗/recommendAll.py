# coding: UTF-8
import tensorflow as tf  
import os  
import numpy as np  
import re  
from PIL import Image  
#import matplotlib.pyplot as plt  
  
  
class NodeLookup(object):  
    def __init__(self):  
        label_lookup_path = r'D:\_CODE\tf\model\imagenet_2012_challenge_label_map_proto.pbtxt'  
        uid_lookup_path = r'D:\_CODE\tf\model\imagenet_synset_to_human_label_map.txt'  
        self.node_lookup = self.load(label_lookup_path, uid_lookup_path)  
  
    def load(self, label_lookup_path, uid_lookup_path):  
        # 加载分类字符串n***********对应分类名称的文件  
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()  
        uid_to_human = {}  
        for line in proto_as_ascii_lines:  
            line = line.strip('\n')  
            parsed_items = line.split('\t')  
            uid = parsed_items[0]  # n15092227  
            human_string = parsed_items[1]  
            uid_to_human[uid] = human_string  
  
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()  
        node_id_to_uid = {}  
        for line in proto_as_ascii:  
            if line.startswith('  target_class:'):  
                target_class = int(line.split(': ')[1])  
            if line.startswith('  target_class_string:'):  
                target_class_string = line.split(': ')[1]  
                node_id_to_uid[target_class] = target_class_string[1: -2]  
  
        node_id_to_name = {}  
        for key, val in node_id_to_uid.items():  
            name = uid_to_human[val]  
            node_id_to_name[key] = name  
  
        return node_id_to_name  
  
    def id_to_string(self, node_id):  
        if node_id not in self.node_lookup:  
            return ''  
        return self.node_lookup[node_id]  
  
  

def fandSame(IDlist,path):    
    result =[]
    # 创建一个图来存放google调整好的模型  
    with tf.gfile.FastGFile('D:/_CODE/tf/model/classify_image_graph_def.pb', 'rb') as f:  
        graph_def = tf.GraphDef()  
        graph_def.ParseFromString(f.read())  
        tf.import_graph_def(graph_def, name='')  
  
    with tf.Session() as sess:  #开始对话
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')  
        # 遍历目录  
        Const_Image_Format = [".jpg",".gif",".png"]
        for root, dirs, files in os.walk( path ):                                       #遍历path
            for file in files:  
                if os.path.splitext(file)[1] in Const_Image_Format :                    #筛选格式！！！！

                    image_data = tf.gfile.FastGFile(os.path.join(root, file), 'rb').read()  
                    predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})  
                    predictions = np.squeeze(predictions)  
  
                    image_path = os.path.join(root, file)  
                    print (image_path)
  
                    #img = Image.open(image_path)  
                    #plt.imshow(img)  
                    #plt.axis('off')  
                    #plt.show()  
  
                    top_k = predictions.argsort()[-5:][::-1]  
                    node_lookup = NodeLookup()  
                    for node_id in top_k:  
                        #human_string = node_lookup.id_to_string(node_id)  
                        #score = predictions[node_id]  
                        if node_id in IDlist:
                            result.append(os.path.join(root, file)) #把符合的路径存上
                            break                                   #退出循环（不然会重复的）
                        #print('%s (score=%.5f)' % (human_string, score))  
                    print()
    return result