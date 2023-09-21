from qiskit.circuit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.accounts.exceptions import AccountNotFoundError
from qiskit_ibm_runtime.api.exceptions import RequestsApiError


if __name__ == "__main__":

    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    bell.measure_all()
    
    channel = "ibm_quantum"
    try:
        service = QiskitRuntimeService(channel=channel)
    except AccountNotFoundError:
        token = input("Please provide your IBM Quantum token: ").strip()
        try:
            service = QiskitRuntimeService(channel=channel, token=token)
        except RequestsApiError as ex:
            if "Error code: 3446" in ex.message:
                raise ValueError("Authentication failed. Make sure the "
                                 "token you passed in is correct.") from None
            raise

    print("Doing quantum magic, please wait...")
    options = {"backend": "ibmq_qasm_simulator"}
    job = service.run(program_id="sampler", 
                      inputs={"circuits":[bell], "resilience_settings":{"level":0}}, 
                      options=options)
    print(job.result())
