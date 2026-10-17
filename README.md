# PFC - Instrumentação de Automodelo (UFMG)

Códigos do projeto de instrumentação do Kyosho Mad Force Kruiser 2.0 VE
para obtenção da curva característica torque × corrente.

## Arquivos
- `Sensor_de_Corrente_ACS758.ino` - firmware do Arduino Due (leitura do sensor ACS758)
- `rodar_ensaio.py` / `rodar_ensaio_desc.py` - escada automática de throttle via Raspberry (subida/descida), grava CSV de corrente
- `teste_throttle.py` - script que roda no Raspberry (PCA9685 -> ESC)
- `planilha_ensaio.xlsx` - planilha de registro e pré-medidas do ensaio

## Uso
1. Rodar `teste_throttle.py` no Raspberry (PCA9685, canal 1, neutro 95°)
2. Notebook: `python3 rodar_ensaio.py` (rede do Pi, ssh sem senha via ssh-copy-id)
3. CSV gerado: `t_ensaio_s;t_degrau_s;angulo;corrente_a`
