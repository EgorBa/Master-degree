# Лабораторная работа 1
### Вариант 7 : [SqueezeNet](https://arxiv.org/abs/1602.07360) и [AmsGrad](https://arxiv.org/abs/1904.09237v1)
***
#### Архитектура SqueezeNet
![SqueezeNet.png](SqueezeNet.png)
***
Тестирование SqueezeNet будет производится на датасете [CarDatasets](https://drive.google.com/drive/folders/1pkudEBabqbXMxRTgfGQs3e0VqfTjtqWU) 
_(для увелечения скорости обучения картинки будут ресайзнуты)_ . Тестирование нейронной сверточной сети на numpy будет производиться на датасете MNIST
***
1. [Реализация SqueezeNet на tensorflow с оптимизатором Adam](Sources/Variant1.ipynb)
2. [Реализация SqueezeNet на tensorflow с оптимизатором AmsGrad](Sources/Variant2.ipynb)
3. [Реализация сверточной нейронной сети на numpy](Sources/CNN.ipynb)
***
#### Выводы по работе
Нейронная сеть на numpy работает медленно, но на датасете MNIST показывает хорошие метрики.
SqueezeNet на CarDatasets показывает не такие хорошие метрики из-за ресайза, 
но при этом отчетливо видно разницу между поведением опитимизаторов. 
На основании экспериментов можно сделать вывод, что Adam дает более хороший результат, 
чем AmsGrad. 
***
Источники, использованные в работе, указаны в виде ссылок
