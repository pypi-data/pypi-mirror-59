# khin1siann1-hun1sik4
輕聲分析器

[![Build Status](https://travis-ci.org/i3thuan5/khin1siann1-hun1sik4.svg?branch=master)](https://travis-ci.org/i3thuan5/khin1siann1-hun1sik4)
[![Coverage Status](https://coveralls.io/repos/github/i3thuan5/khin1siann1-hun1sik4/badge.svg?branch=master)](https://coveralls.io/github/i3thuan5/khin1siann1-hun1sik4?branch=master)

計算台語詞頻的輕聲分析工具。根據詞彙分級網站需要的詞頻書寫規則，判斷一句話內底的輕聲詞的斷詞。

### 詞頻書寫是？

詞頻書寫是算詞頻用的羅馬字書寫規範。詞頻書寫毋是完全照教育部書寫，比如講等我：

- 教育部書寫：tan2--gua2
- 詞頻書寫：tan2 --gua2

教育部書寫有規定，輕聲符一定kah頭前的詞連寫；詞頻書寫愛看狀況，將非詞組的詞用空白隔開，方便計算詞頻。


## 開發

### 試驗

```
python -m unittest 
```

### 輕聲詞資料

紀錄輕聲詞屬啥款情形
- 分寫
  - 佮頭前詞分開
- 連寫
  - 佮頭前詞相接
- 不處理
- 動詞補語

動詞補語的用法較複雜，所致目前嘛làng過無處理。親像「leh」：
- 拭拭咧 tshit-tshit--eh，連寫，疊字詞+咧
- 看覓咧 khuànn-māi --eh，分寫，動詞+咧
- 佇咧 tī--eh，連寫，詞彙化
