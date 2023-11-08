for py in OrderMonitor.py BatchOrderMonitor.py OrderMonitorNetting.py TableListenerContainer.py common.py 
do
    echo " # $py" >> jgtfxcommon.py
    cat common_samples/$py >> jgtfxcommon.py

    echo "#------------------------#" >> jgtfxcommon.py
done