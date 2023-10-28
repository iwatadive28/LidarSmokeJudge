import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation


# 霧判定
import LidarSmokeJudge

# パラメータ
params_is_insmoke = {
    'D': 5.0,
    'thresh_valid': 0.75, # 以下
    'thresh_zero': 0.60, # 以上
    'max_points_num':28800
}

params_smoke_filt = {
    'D': 12.0,      # 距離
    'I': 8,         # 強度
    'Z': 0.5,       # 路面からの高さ閾値
    'SetPosX': 0.0, # LiDAR設置位置
    'SetPosY': 0.0, 
    'SetPosZ': 2.0,
}
lidar_smoke_judge = LidarSmokeJudge.LidarSmokeJudge(params_is_insmoke, params_smoke_filt)

# 初期化関数
def init():
    pass

# テストコード
class LiDARVisualizer:
    def __init__(self, data_dir, start_frame, end_frame, z_range=(-2,2)):
        self.data_dir = data_dir
        self.file_extension = '*.txt'
        self.start_frame = start_frame
        self.end_frame = end_frame
        
        self.frame_num = -1
        self.frame_interval = 100 # フレームごとの表示間隔（ミリ秒）
        
        self.cmap = plt.get_cmap('jet')   # カラーマップの設定
        self.norm = plt.Normalize(-2, 2)  # カラーバーの範囲を0から3に設定
        
        self.xlim = (-20,20)
        self.ylim = (-20,20)
        self.zlim = z_range
        
        self.fig = plt.figure()

    def scatter_graph(self,x,y,z):
        
        frame_num = self.frame_num
        # 散布図プロット
        sc = plt.scatter(x, y, c=z, cmap=self.cmap, norm=self.norm, marker='.', label='LiDAR Points')
        
        plt.xlabel('X')
        plt.xlabel('Y')        
        plt.title(f'Frame {frame_num}')
        
        plt.grid()
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)
        
        # 第1系列のカラーバーを設定する。
        cbar = plt.colorbar(sc)
        cbar.set_label('Z Value')
        
        # カラーバーの範囲を設定
        cbar.set_clim(self.z_range) 
        
        # 軸の比率を1:1に設定
        plt.gca().set_aspect('equal', adjustable='box')
    
    # 霧判定してプロット
    def scatter_graph_smoke(self,cells_lidar):
        
        is_insmoke, valid_idx, valid_ratio, zero_ratio = lidar_smoke_judge.is_in_smoke(cells_lidar)
        smoke_idx = lidar_smoke_judge.smoke_filter(cells_lidar)

        x = cells_lidar['X']
        y = cells_lidar['Y']
        
        frame_num = self.frame_num
        
        # 散布図プロット
        sc = plt.scatter(x, y, c='k', marker='.', label='LiDAR Points with Smoke Judge')
        
        plt.scatter(x[valid_idx], y[valid_idx], c='g',s=10)
        plt.scatter(x[smoke_idx], y[smoke_idx], c='r',s=10)
        
        if is_insmoke:
            plt.text(self.xlim[0]+1, self.ylim[1]-1, 'In Smoke', color='r')
        
        plt.xlabel('X')
        plt.ylabel('Y')
        
        ttl_valid_ratio = f"valid-ratio = {valid_ratio*100:.2f}[%]"
        ttl_zero_ratio  = f"zero-ratio = {zero_ratio*100:.2f}[%]"
        ttl_frame       = f'Frame {frame_num}'
        ttl = ttl_frame + "," + ttl_valid_ratio + "," + ttl_zero_ratio
        plt.title(ttl)
        
        plt.grid()
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)
        
        # 軸の比率を1:1に設定
        plt.gca().set_aspect('equal', adjustable='box')   
    
    def plot_frame(self, frame_num):
        fig = self.fig
        fig.clear()
        
        frame_num += start_frame
        self.frame_num = frame_num
        
        file_name = f"{frame_num:d}{'_'}{self.file_extension}"
        file_path  = glob.glob(f"{self.data_dir}{'/'}{file_name}")
        if len(file_path) == 0:
            print('END')
            exit()
            
        file_path = file_path[0]
        print(file_path)
        
        if frame_num == self.end_frame-1:
            print('END')
            # exit()
        
        if os.path.exists(file_path):
            # データ読み出し
            data = np.genfromtxt(file_path, delimiter=',', names=True, dtype=None)
            x = data['X']
            y = data['Y']
            z = data['Z']
            I    = data['intensity']
            Dist = data['distance']
            Time = data['time']
            Azim = np.rad2deg(np.arctan2(-x,y))
            # Azim = np.rad2deg(np.arctan2(y,x))
            Elev = np.rad2deg(np.arcsin(z/Dist))
            
            # 散布図プロット
            # self.scatter_graph(x,y,z)
                        
            # 霧判定
            cells_lidar = {
                'Dist': Dist,
                'Azim': Azim,
                'Elev': Elev,
                'I':    I,
                'X':    x,
                'Y':    y,
                'Z':    z
            }
            
            # 霧判定プロット
            self.scatter_graph_smoke(cells_lidar)
            
            # import pdb; pdb.set_trace()
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
    data_dir = '../data/smoke3/velodynevlp16/data_ascii'
    start_frame = 200
    end_frame = 250
    visualizer = LiDARVisualizer(data_dir, start_frame, end_frame)
    visualizer.visualize_frames()
    