for i in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
do 
./train_fast.sh adv both $i
./train_fast.sh victim both $i
done

./perf_test_all.sh
