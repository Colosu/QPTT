# QPTT
Quantum Programs Testing Tool

Repositorio del grupo 3 de la Qiskit Hackathon Madrid 2021.

El objetivo de este proyecto es crear una herramienta que reciba un circuito cuántico, un valor inicial para los qubits de entrada (llamado input) y una distribución de resultados esperada (llamado oráculo). El programa debe procesar el input para crear un valor inicial para todos los qubits del programa, ejecutarlo múltiples veces para obtener una distribución de resultados (llamada output), y finalmente comparar el output y el oráculo, con métodos estadísticos, para determinar si ambas distribuciones son equivalentes.

La totalidad del código se encuentra en el fichero QPTT.ipynb. Una versión preparada para ser usada como librería se puede encontrar en el fichero QPTT.py.

La función principal es la función QPTT que recibe:
- El circuito cuántico a testear.
- El número de qubits que son inputs.
- El oráculo en formato diccionario en el que a cada input que se quiere testear le asigne otro diccionario en el que a cada posible output le asigne una probabilidad.
- Opcionalmente, los ínputs en un array que contenga los inputs en formato array de unos y ceros. Por defecto, el programa usa como inputs la superposición de todos los posibles inputs.
