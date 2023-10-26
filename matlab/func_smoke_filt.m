function smoke_idx = func_smoke_filt(cells_lidar,params_smoke_filt);
% func_smoke_filt
% 霧フィルタ：霧の可能性がある点群を除去
% 霧らしい点群にフラグを立てる
       
filt_dist = cells_lidar.Dist(:) < params_smoke_filt.D;
filt_I    = cells_lidar.I  < params_smoke_filt.I;
filt_Z    = cells_lidar.Z + params_smoke_filt.SetPosZ > params_smoke_filt.Z;

smoke_idx = filt_dist & filt_I &  filt_Z;
end

