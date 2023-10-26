function [is_insmoke, valid_idx, valid_ratio, zero_ratio]= func_is_insmoke(cells_lidar,params_is_insmoke);
% func_is_insmoke
% is_insmoke : (bool) 霧の中にいるか？
% valid_ratio : (double) 有効な点群の割合 0~1 %
% zero_ratio : (double) ゼロ埋めされている点群の割合 0~1 %

% 前方() D以上の点群数が~%以上か？
filt_dist = cells_lidar.Dist(:) >  params_is_insmoke.D;

% 前方の点を有効な点とする
% 前方かつDist非ゼロの点をそのフレームの有効な点数とする
filt_front = abs( cells_lidar.Azim(:)) < 90 ;
filt_d0    = cells_lidar.Dist(:) == 0;
front_points_num = nnz(filt_front & ~filt_d0); % 前方かつDist非ゼロ

valid_idx  = filt_dist & filt_front; % 有効な点
valid_num  = nnz(valid_idx); 

% 割合
valid_ratio = valid_num/front_points_num; % 有効な点群の割合 0~1
zero_ratio  = nnz(filt_front & filt_d0) / nnz(filt_front); % 前方の点のうちゼロ埋めされている点群の割合 0~1

% 判定
is_insmoke_valid = valid_ratio < params_is_insmoke.thresh_valid;
is_insmoke_zero  = zero_ratio  > params_is_insmoke.thresh_zero ;

is_insmoke = is_insmoke_valid | is_insmoke_zero;

end

