# Лабораторная работа 1
### Вариант 7 : [SqueezeNet](https://arxiv.org/abs/1602.07360) и [AmsGrad](https://arxiv.org/abs/1904.09237v1)
***
#### Архитектура SqueezeNet
![SqueezeNet.png](SqueezeNet.png)
***
Тестирование производится на датасете [CarDatasets](https://drive.google.com/drive/folders/1pkudEBabqbXMxRTgfGQs3e0VqfTjtqWU) 
_(для увелечения скорости обучения картинки будут ресайзнуты)_
***
1. [Реализация SqueezeNet на tensorflow с оптимизатором Adam](Sources/Variant1.ipynb)
2. [Реализация SqueezeNet на tensorflow с оптимизатором AmsGrad](Sources/Variant2.ipynb)
***
#### Выводы по работе
Метрики по результатам экспериментов отличаются не сильно, а значит
для достяжения более хороших резльтатов надо менять архитектуру сети.
Хоть и оптимизотор Adam дает более хороший результат, чем AmsGrad, этого 
все равно не достаточно. 
***
Источники, использованные в работе, указаны в виде ссылок
