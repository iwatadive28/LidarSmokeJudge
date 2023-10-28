import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 初期化関数
def init():
    pass

# テストコード
class LiDARVisualizer:
    def __init__(self, data_dir, start_frame, end_frame, z_range=(-2,2)):
        self.data_dir = data_dir
        self.files = glob.glob(data_dir + '/*.txt')
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.z_range = z_range
        
        self.frame_interval = 100 # フレームごとの表示間隔（ミリ秒）
        
        # カラーマップの設定
        self.cmap = plt.get_cmap('jet')
        self.norm = plt.Normalize(-2, 2)  # カラーバーの範囲を0から3に設定
        
        self.fig = plt.figure()
        
    def plot_frame(self, frame_num):
        fig = self.fig
        fig.clear()
        
        frame_num += start_frame
        file_path = self.files[frame_num]
            
        if os.path.exists(file_path):
            data = np.genfromtxt(file_path, delimiter=',', names=True, dtype=None)
            x = data['X']
            y = data['Y']
            z = data['Z']
            
            sc = plt.scatter(x, y, c=z, cmap=self.cmap, norm=self.norm, marker='.', label='LiDAR Points')
            
            plt.xlabel('X')
            plt.xlabel('Y')        
            plt.title(f'Frame {frame_num}')
            
            plt.grid()
            plt.xlim(-20,20)
            plt.ylim(-20,20)
            
            # 第1系列のカラーバーを設定する。
            cbar = plt.colorbar(sc)
            cbar.set_label('Z Value')
            
            # カラーバーの範囲を設定
            cbar.set_clim(self.z_range) 
            
            # 軸の比率を1:1に設定
            plt.gca().set_aspect('equal', adjustable='box')
            
        else:
            print(f"File not found: {file_path}")
            
    def visualize_frames(self):
        # アニメーションを作成
        ani = FuncAnimation(self.fig,\
                            self.plot_frame, \
                            frames=range(self.end_frame - self.start_frame + 1),\
                            init_func=init,\
                            blit=False,\
                            repeat=True,\
                            interval=self.frame_interval)
        plt.show()
        
if __name__ == "__main__":
    # データが保存されているディレクトリのパス
    data_dir = '../work/veloparser/tmp/velodynevlp16/data_ascii'
    start_frame = 1
    end_frame = 1
    visualizer = LiDARVisualizer(data_dir, start_frame, end_frame)
    visualizer.visualize_frames()
    