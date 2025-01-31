import multiprocessing
import os

# ==============================
# 🔥 CONFIGURAÇÕES DE OTIMIZAÇÃO
# ==============================

# Bind -> Gunicorn escutará apenas localmente para ser usado atrás do Nginx
bind = "127.0.0.1:8000"

# Workers -> Número ideal de processos baseados no número de núcleos de CPU
workers = multiprocessing.cpu_count() * 2 + 1  # Regra recomendada

# Worker Class -> Usamos "gthread" para APIs, pois suporta requisições concorrentes melhor
worker_class = "gthread"

# Threads -> Define quantas threads cada worker pode usar (bom para APIs REST)
threads = 4  # Ajustável dependendo da carga

# Tempo máximo para resposta (evita travamento)
timeout = 30  # Fecha requisições lentas após 30 segundos

# Keepalive -> Mantém conexões abertas para reutilização, melhorando a performance
keepalive = 5

# Limita o número de conexões simultâneas para evitar sobrecarga
worker_connections = 1000

# ==============================
# 📜 LOGS PARA MONITORAMENTO
# ==============================

# Ativa os logs de acesso e erro
accesslog = "./logs/gunicorn/access.log"
errorlog = "./logs/gunicorn/error.log"

# Nível de log -> "info" é um bom equilíbrio entre detalhes e desempenho
loglevel = "info"

# ==============================
# 📈 OTIMIZAÇÕES ADICIONAIS
# ==============================

# Fecha conexões inativas para liberar memória
graceful_timeout = 30  # Se o worker não responder, ele será reiniciado

# Desativa o daemon (melhor rodar com systemd)
daemon = False

# Maximiza desempenho desativando buffers desnecessários no Gunicorn
preload_app = True  # Carrega a aplicação antes de criar os workers

# Melhora o tempo de resposta reduzindo a troca de contexto
limit_request_line = 4094  # Aumenta o tamanho máximo da linha de requisição

# ==============================
# 🔄 GERENCIAMENTO AUTOMÁTICO
# ==============================

# Se um worker travar, o Gunicorn o reiniciará automaticamente
max_requests = 1000  # Reinicia worker após X requisições (evita vazamento de memória)
max_requests_jitter = 50  # Evita que todos os workers reiniciem ao mesmo tempo

