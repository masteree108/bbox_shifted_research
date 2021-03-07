---
title: 'openCV tracker 研究低fps bounding box 偏移解決方法'
disqus: hackmd
---

penCV tracker 研究低fps bounding box 偏移解決方法(ubuntu18.04)
===

文件版本.：v0.0.1
[TOC]





## 1. 筆記解說

目前測試低fps(5fps),會有bounding box 偏移的現象,如下影片
https://youtu.be/5ZPR2aXiDEM


若是 使用 29.97fps 無此現象
https://youtu.be/vu9Y9_2dlnM




## 2. 測試 source code
至此 [github](https://github.com/masteree108/bbox_shifted_research) 可下載 測試程式

s選完一個人物後按下 Enter,
然後選下一個按一次 Enter
最後按下 ESC 讓程式繼續運作


### 5fps 測試方法
如下圖選擇 07_clip_5fps.mp4
![](https://i.imgur.com/NdzqPqs.png)

```
$ conda activate your_python_container
$ ./run.py
```

### 29.97 fps 測試方法
如下圖選擇 07_clip_30fps.mp4
![](https://i.imgur.com/g2SrEgr.png)

```
$ conda activate your_python_container
$ ./run.py
```

###### tags: `study`, `VoTT`
