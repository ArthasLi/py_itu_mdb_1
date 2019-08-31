mtr = load('band_map.txt');
max_v = max(max(mtr));
mtr = mtr/max_v;
dim = size(mtr)
for i = 1:dim(1)
    for j = 1:dim(2)
        mtr(i,j) = (1-mtr(i,j))^2*100;
    end
end
mtr
