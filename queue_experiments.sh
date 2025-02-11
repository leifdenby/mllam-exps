# create a list of train_duration values, with increments in years from 1 to 5 in iso8601 format
train_duration=(P1Y P2Y P3Y)

# for testing purposes, we will use weeks instead of years
# train_duration=(P2W)

# queue up the experiments with dvc
for duration in ${train_duration[@]}; do
    dvc exp run --queue -S train_duration=${duration}
done