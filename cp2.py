import cv2
import mediapipe as mp
import time
import random

# Inicializações

# MediaPipe para rastreamento da mão
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Carregamento das imagens
dardo_img = cv2.resize(cv2.imread("dardo.png"), (50, 50))
inimigo_img = cv2.resize(cv2.imread("inimigo.png"), (60, 60))

# Listas para controlar objetos em jogo
dardos = []
inimigos = []

# Temporizadores para limitar ações
ultimo_disparo = 0
ultimo_spawn = 0

# Contador de inimigos abatidos
inimigos_abatidos = 0

# Tempo de início da partida
inicio_partida = time.time()

# Loop principal do jogo 
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar vídeo ou vídeo finalizado.")
        break

    # Tamanho da janela
    frame = cv2.resize(frame, (640, 960))

    # Conversão para RGB 
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado_mao = hands.process(frame_rgb)

    # Calcula tempo de jogo e ajusta dificuldade
    tempo_atual = time.time()
    tempo_decorrido = tempo_atual - inicio_partida

    # Diminui o delay gradualmente 
    delay_disparo =  0.5 * (0.98 ** inimigos_abatidos)
    delay_spawn =  1.0 * (0.96 ** inimigos_abatidos)

    # Rastreia a mão 

    dedo_levantado = False
    dedo_x, dedo_y = None, None

    if resultado_mao.multi_hand_landmarks:
        for mao in resultado_mao.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, mao, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            dedo_x = int(mao.landmark[8].x * w)
            dedo_y = int(mao.landmark[8].y * h)

            if mao.landmark[8].y < 0.5:
                dedo_levantado = True



    # Disparo de dardos
    if dedo_levantado and dedo_x is not None:
        if tempo_atual - ultimo_disparo >= delay_disparo:
            dardos.append({"x": dedo_x, "y": dedo_y})
            ultimo_disparo = tempo_atual



    # Geração de inimigos
    if tempo_atual - ultimo_spawn >= delay_spawn:
        inimigo_x = random.randint(60, 640 - 60)
        # Começa fora da tela(valor negativo)
        inimigos.append({"x": inimigo_x, "y": -60}) 
        ultimo_spawn = tempo_atual



    #  Atualiza Dardos
    novos_dardos = []  

    for dardo in dardos:
        # Move o dardo para cima 
        dardo["y"] -= 30  

        # Se o dardo ainda não saiu completamente da tela, continua desenhando
        if dardo["y"] > -dardo_img.shape[0]:
            novos_dardos.append(dardo)  # Mantém o dardo ativo

            # Centraliza o dardo baseado na mão
            dx = dardo["x"] - 25
            dy = dardo["y"] - 25

            # Garante que o dardo será desenhado apenas se estiver dentro da área visível da tela
            if 0 <= dx <= frame.shape[1] - 50 and 0 <= dy <= frame.shape[0] - 50:
                # Seleciona a região onde o dardo será desenhado
                roi = frame[dy:dy + 50, dx:dx + 50]

                # Cria uma máscara para remover o fundo da imagem do dardo
                mask = cv2.threshold(cv2.cvtColor(dardo_img, cv2.COLOR_BGR2GRAY), 10, 255, cv2.THRESH_BINARY)[1]

                # Remove o fundo do ROI onde o dardo será desenhado
                bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))
                # Pega somente o dardo com base na máscara
                fg = cv2.bitwise_and(dardo_img, dardo_img, mask=mask)

                # Combina o fundo com o dardo e atualiza no frame
                frame[dy:dy + 50, dx:dx + 50] = cv2.add(bg, fg)

    # Atualiza a lista de dardos com apenas os que ainda estão ativos
    dardos = novos_dardos


    # Atualiza Inimigos e Verifica Colisões 
    novos_inimigos = []

    # Para cada inimigo atual na tela
    for inimigo in inimigos:
        # Move o inimigo para baixo
        inimigo["y"] += 5

        # Calcula a posição de desenho do inimigo 
        ix = inimigo["x"] - 30  # Largura da imagem é 60
        iy = inimigo["y"]

        # Verifica se o inimigo ainda está dentro da tela
        if iy < 960:
            colidiu = False  # Flag para saber se colidiu com algum dardo

            # Verifica colisão com todos os dardos
            for dardo in dardos:
                # Se a distância entre o centro do dardo e do inimigo for pequena o suficiente, considera colisão
                if abs(dardo["x"] - inimigo["x"]) < 30 and abs(dardo["y"] - inimigo["y"]) < 30:
                    colidiu = True
                    inimigos_abatidos += 1  # Incrementa o contador de abates
                    break  

            # Se não colidiu com nenhum dardo, o inimigo continua na tela
            if not colidiu:
                novos_inimigos.append(inimigo)

                # Verifica se o inimigo está em uma posição válida para desenhar (evita erro de borda da imagem)
                if 0 <= ix <= frame.shape[1] - 60 and 0 <= iy <= frame.shape[0] - 60:
                    # Região onde o inimigo estará no frame
                    roi = frame[iy:iy + 60, ix:ix + 60]

                    # Cria uma máscara para recortar apenas o inimigo (removendo fundo preto da imagem)
                    mask = cv2.threshold(cv2.cvtColor(inimigo_img, cv2.COLOR_BGR2GRAY), 10, 255, cv2.THRESH_BINARY)[1]

                    # Separa fundo e imagem do inimigo com base na máscara
                    bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))
                    fg = cv2.bitwise_and(inimigo_img, inimigo_img, mask=mask)

                    # Sobrepõe a imagem do inimigo no frame
                    frame[iy:iy + 60, ix:ix + 60] = cv2.add(bg, fg)

    # Atualiza a lista de inimigos com apenas os que continuam vivos/ativos
    inimigos = novos_inimigos


    # HUD 
   
    cv2.putText(frame, f"Tempo: {int(tempo_decorrido)}s", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Estouros: {inimigos_abatidos}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f"Delay Tiro: {delay_disparo:.2f}s", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(frame, f"Delay Inimigo: {delay_spawn:.2f}s", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Jogo de estourar balão", frame)
    
    # Sai do jogo com 'q' ou ESC
    if cv2.waitKey(30) & 0xFF in [ord('q'), 27]:
        break

# Finaliza o jogo
cap.release()
cv2.destroyAllWindows()
