#!/usr/bin/env python
# coding: utf-8

import numpy as np
import scipy.stats as st

# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile, Aer, IBMQ, execute
from qiskit.tools.jupyter import *
from qiskit.visualization import *
#from ibm_quantum_widgets import *
from qiskit.providers.aer import QasmSimulator
from qiskit.tools.visualization import plot_histogram

def qc1():
    
    input_qubit = QuantumRegister(2, 'input_qubit')
    output_qubit = QuantumRegister(1, 'output_qubit')
    c = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(input_qubit, output_qubit, c)
    # Implementation statements
    qc.h(output_qubit)
    qc.cswap(output_qubit, input_qubit[0], input_qubit[1])
    qc.h(output_qubit)
    qc.x(output_qubit)
    qc.measure(output_qubit, c)
    
    return qc

def qc2():
    
    input_qubit = QuantumRegister(2, 'input_qubit')
    output_qubit = QuantumRegister(1, 'output_qubit')
    c = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(input_qubit, output_qubit, c)
    # Implementation statements
    qc.ccx(input_qubit[0], input_qubit[1], output_qubit)
    qc.measure(output_qubit, c)
    
    return qc

#Función test_input_generator
#INPUTS: num_input_qubits: int, mode: string, test_list: array of ints
#OUTPUTS: input_array: array of arrays of ints
def test_input_generator(num_input_qubits=0, mode="auto", test_list=[]):

    input_array = []
    
    if mode == "auto":
        for i in range(2**num_input_qubits):
            bin_array = [int(x) for x in list('{0:{fill}{width}b}'.format(i, fill=0, width=num_input_qubits))]
            input_array.append(bin_array)
    elif mode == "custom":
        for i in test_list:
            bin_array = [int(x) for x in list('{0:{fill}{width}b}'.format(i, fill=0, width=num_input_qubits))]
            input_array.append(bin_array)
        
    return input_array

#Función iqc_individual
#INPUTS: value: array of ints, num_total_qubits: int, num_cl_bits: int
#OUTPUTS: qc: QuantumCircuit
def iqc_individual(value=[], num_total_qubits=0, num_cl_bits=0):

    num_input_qubits = len(value)
    
    qr = QuantumRegister(num_total_qubits)
    cr = ClassicalRegister(num_cl_bits)
    
    qc = QuantumCircuit(qr, cr)
    
    index = 0
    
    for bit in value:
        if (bit == 1):
            qc.x(index)
        index += 1
    
    qc.barrier()
    return qc

#Función iqc_superposition
#INPUTS: num_inputs: int, num_total_qubits: int, num_cl_bits: int
#OUTPUTS: qc: QuantumCircuit
def iqc_superposition(num_inputs=0, num_total_qubits=0, num_cl_bits=0):
    
    qr = QuantumRegister(num_total_qubits)
    cr = ClassicalRegister(num_cl_bits)
    
    qc = QuantumCircuit(qr, cr)
    
    qc.barrier()
    
    index = 0
    #qc.x(index)
    #qc.x(index+1)
    
    for bit in range(num_inputs):
        qc.h(index)
        index += 1
    
    qc.barrier()
    return qc

#Función test_circuit
#INPUTS: iqc: QuantumCircuit, qc: QuantumCircuit, shots: int
#OUTPUTS: histogram: array of ints
def test_circuit(iqc, qc,  shots=1024):
    fqc = iqc.compose(qc)
    
    emulator = Aer.get_backend('qasm_simulator')
    job = execute(fqc, emulator, shots=shots) 

    # The result is a histogram in the form of a dictionary.
    histogram = job.result().get_counts()
    #print ('results: ', histogram)

    # plot histogram
    #legend = ['Execution results']
    #plot_histogram(histogram,legend=legend)
    
    return histogram

#Función oracle_union
#INPUTS: oracles: dict<string, dict<string, int>>
#OUTPUTS: oracle: dict<string, int>
def oracle_union(oracles):
    oracle = {}
    iters = 0
    for key, value in oracles.items():
        for k, v in value.items():
            if k in oracle:
                oracle[k] += v
            else:
                oracle[k] = v
        iters += 1
    for key, value in oracle.items():
        oracle[key] = int(oracle[key]/iters) 
    return oracle

#Función chi_square
#INPUTS: outputs: dict<string, int>, oracle: dict<string, int>
#OUTPUTS: boolean
def chi_square(outputs,oracle):
    if len(oracle) > 1 and len(outputs) > 1:
        alpha = 0.05
        outputs = [outputs[key] for key in sorted(outputs.keys())]
        oracle = [oracle[key] for key in sorted(oracle.keys())]
        #outputs = outputs/np.sum(outputs)
        #oracle = oracle/np.sum(oracle)
        stat, pvalue = st.chisquare(outputs,oracle)
        #print("H-value: " + str(stat))
        #print("p-value: " + str(pvalue))
        #print()
        if pvalue > alpha:
            #print('Dependent (reject H0)')
            return True
        else:
            #print('Independent (fail to reject H0)')
            return False
    else:
        if oracle.keys() == outputs.keys():
            return True
        else:
            return False

#Función QPTT
#INPUTS: qc: QuantumCircuit, num_inputs: int, oracles: dict<string, dict<string, int>>, inputs_array: array of arrays of ints, shots: int
#OUTPUTS: void
def QPTT(qc, num_inputs, oracles, inputs_array=None, shots=1024):
    
    if inputs_array != None:
        for inputs,oracle in zip(inputs_array,oracles.values()):
            # Get total number of qubits and classical bits
            num_total_qubits = qc.num_qubits
            num_cl_bits = qc.width() - num_total_qubits

            # Go through the test value array and execute the test
            #for value in input_array:
            #    print(value)
            #    iqc = input_quantum_circuit(value=value, num_total_qubits=num_total_qubits, num_cl_bits=num_cl_bits)
            #    test_circuit(iqc,qc)

            iqc = iqc_individual(value=inputs, num_total_qubits=num_total_qubits, num_cl_bits=num_cl_bits)
            outputs = test_circuit(iqc,qc,shots)
            result = chi_square(outputs, oracle)
            if result:
                print(f"Circuit passed evaluation for input {inputs}.")
            else:
                print(f"Circuit failed evaluation for input {inputs}! There is some error.")
                print(f"Circuit returned {outputs}")
    else:
        oracle = oracle_union(oracles)
        # Get total number of qubits and classical bits
        num_total_qubits = qc.num_qubits
        num_cl_bits = qc.width() - num_total_qubits

        # Go through the test value array and execute the test
        #for value in input_array:
        #    print(value)
        #    iqc = input_quantum_circuit(value=value, num_total_qubits=num_total_qubits, num_cl_bits=num_cl_bits)
        #    test_circuit(iqc,qc)

        iqc = iqc_superposition(num_inputs=num_inputs, num_total_qubits=num_total_qubits, num_cl_bits=num_cl_bits)
        outputs = test_circuit(iqc,qc,shots)
        result = chi_square(outputs, oracle)
        if result:
            print(f"Circuit passed evaluation.")
        else:
            print(f"Circuit failed evaluation! There is some error.")
            print(f"Circuit returned {outputs}")


