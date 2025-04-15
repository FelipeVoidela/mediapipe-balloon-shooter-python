# Integrantes do grupo 

Felipe Voidela RM98595

Gustavo Ozeki RM98481

Ian Cancian Nachtergaele RM98387

# Jogo Interativo de Estourar Balões com Controle por Mão

## Descrição

O **Jogo Interativo de Estourar Balões** é uma aplicação divertida e educativa que combina **visão computacional** com **interação física**, usando a **webcam** para detectar a mão do jogador e um **Arduino** para fornecer **feedback com LEDs e som**.

O jogador deve levantar o dedo indicador para lançar dardos e **acertar inimigos que descem pela tela**. A dificuldade aumenta conforme o número de inimigos abatidos, tornando a experiência mais desafiadora. LEDs coloridos e um buzzer são usados para indicar o progresso do jogador com **alertas visuais e sonoros**.

---

## Tecnologias Utilizadas

- **OpenCV** — Captura de vídeo e exibição em tempo real.
- **MediaPipe** — Rastreia a mão e identifica a posição do dedo indicador.
- **Arduino** — Controla LEDs e o buzzer para alertas físicos.
- **Python** — Lógica do jogo e comunicação serial com o Arduino.

---

## Como Funciona

- O jogo detecta quando o **dedo indicador está levantado** para lançar um dardo.
- Os inimigos (balões) aparecem aleatoriamente no topo da tela e descem.
- Quando um dardo atinge um inimigo, ele é removido da tela e o placar aumenta.
- Conforme o número de inimigos abatidos aumenta, o intervalo de disparo e o surgimento de inimigos diminuem — aumentando a dificuldade.
- O **Arduino** fornece **feedback físico**:
  - **LED Verde**: menos de 10 inimigos abatidos.
  - **LED Amarelo**: entre 11 e 50 inimigos abatidos.
  - **LED Vermelho**: mais de 100 inimigos abatidos.

---

## Aplicações Reais

Este projeto pode ser utilizado em:

- Treinamento de coordenação motora e reflexos.
- Projetos de demonstração de integração Python + Arduino.
- Atividades educativas envolvendo computação física e visão computacional.

---

## Como Rodar

### Requisitos

- **Python 3.x**
- **Arduino Uno ou compatível**
- **Bibliotecas Python**:
  - `opencv-python`
  - `mediapipe`
  - `pyserial`

### Instalação das Dependências

```bash
pip install opencv-python mediapipe pyserial
