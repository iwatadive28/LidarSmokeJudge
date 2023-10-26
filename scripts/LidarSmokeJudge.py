import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

class LidarSmokeJudge:
    def __init__(self, params_is_insmoke, params_smoke_filt):
        self.params_is_insmoke = params_is_insmoke
        self.params_smoke_filt = params_smoke_filt

    def is_in_smoke(self, cells_lidar):
        # is_in_smoke
        # is_insmoke : (bool) 霧の中にいるか？
        # valid_ratio : (double) 有効な点群の割合 0~1 %
        # zero_ratio : (double) ゼロ埋めされている点群の割合 0~1 %

        # 前方() D以上の点群数が~%以上か？
        filt_dist = cells_lidar['Dist']  > self.params_is_insmoke['D']
        
        # 前方の点を有効な点とする
        # 前方かつDist非ゼロの点をそのフレームの有効な点数とする
        filt_front = np.abs(cells_lidar['Azim']) < 90
        filt_d0 = cells_lidar['Dist'] == 0
        front_points_num = np.count_nonzero(filt_front & ~filt_d0)


        valid_idx = filt_dist & filt_front      # 有効な点
        valid_num = np.count_nonzero(valid_idx)

        # 割合
        valid_ratio = valid_num / front_points_num # 有効な点群の割合 0~1
        zero_ratio = np.count_nonzero(filt_front & filt_d0) / np.count_nonzero(filt_front) # 前方の点のうちゼロ埋めされている点群の割合 0~1

        # 判定
        is_insmoke_valid = valid_ratio < self.params_is_insmoke['thresh_valid']
        is_insmoke_zero = zero_ratio > self.params_is_insmoke['thresh_zero']

        is_insmoke = is_insmoke_valid or is_insmoke_zero

        return is_insmoke, valid_idx, valid_ratio, zero_ratio

    def smoke_filter(self, cells_lidar):
        # smoke_filter
        # 霧の可能性がある点群を除去する関数

        filt_dist = cells_lidar['Dist']  < self.params_smoke_filt['D']
        filt_I = cells_lidar['I'] < self.params_smoke_filt['I']
        filt_Z = cells_lidar['Z'] + self.params_smoke_filt['SetPosZ'] > self.params_smoke_filt['Z']
        smoke_idx = filt_dist & filt_I & filt_Z
        return smoke_idx

# テストコード
def test():
    params_is_insmoke = {
        'D': 5.0,
        'thresh_valid': 0.75, # 以下
        'thresh_zero': 0.60 # 以上
    }

    params_smoke_filt = {
        'D': 12.0,      # 距離
        'I': 8,         # 強度
        'Z': 0.5,       # 路面からの高さ閾値
        'SetPosX': 0.0, # LiDAR設置位置
        'SetPosY': 0.0, 
        'SetPosZ': 2.0,
    }

    num_points = 100
    max_D = 30
    Dist = max_D/2 * np.random.randn(num_points) + max_D/2
    Azim = 180 * np.random.randn(num_points)
    Elev = 15 * np.random.randn(num_points)
    I    = np.random.randint(1,63,num_points)
    X    = Dist * np.cos(np.deg2rad(Elev)) * np.cos(np.deg2rad(Azim))
    Y    = Dist * np.cos(np.deg2rad(Elev)) * np.sin(np.deg2rad(Azim))
    Z    = Dist * np.sin(np.deg2rad(Elev)) 

    cells_lidar = {
        'Dist': Dist,
        'Azim': Azim,
        'Elev': Elev,
        'I':    I,
        'X':    X,
        'Y':    Y,
        'Z':    Z
    }

    lidar_smoke_judge = LidarSmokeJudge(params_is_insmoke, params_smoke_filt)
    is_insmoke, valid_idx, valid_ratio, zero_ratio = lidar_smoke_judge.is_in_smoke(cells_lidar)
    smoke_idx = lidar_smoke_judge.smoke_filter(cells_lidar)

    print("is_insmoke:", is_insmoke)
    print("valid_idx:", valid_idx)
    print("valid_ratio:", valid_ratio)
    print("zero_ratio:", zero_ratio)
    print("smoke_idx:", smoke_idx)

    
    # グラフ表示
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ax.scatter(X, Y, Z, c='k',s=8)
    # ax.grid(which='minor')
    
    ax.hold(True)
    ax.scatter(X[valid_idx], Y[valid_idx], Z[valid_idx], c='g',s=10)
    ax.scatter(X[smoke_idx], Y[smoke_idx], Z[smoke_idx], c='r',s=10)
    ax.hold(False)
    
    if is_insmoke:
        ax.text(19, 29, 0,'In Smoke', color='r')

    # 軸ラベルの設定
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 表示範囲の設定
    ax.set_xlim(-30, 30)
    ax.set_ylim(-20, 20)
    ax.set_zlim(-5 ,5 )
    
    ax.view_init(90,0)
    
    ttl_valid_ratio = f"valid-ratio = {valid_ratio*100:.2f}[%]"
    ttl_zero_ratio = f"zero-ratio = {zero_ratio*100:.2f}[%]"
    ax.set_title(ttl_valid_ratio + ttl_zero_ratio)
    
    plt.show()
    
if __name__ == "__main__":
    test()