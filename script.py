import streamlit
import streamlit as st
import google.generativeai as genai


api_key = st.secrets("API_KEY")
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Erro ao carregar o modelo Gemini 'gemini-2.0-flash': {e}")
    st.info("Verifique se o nome do modelo está correto e se sua chave API tem acesso a ele.")
    st.stop()

def gerar_resposta_gemini(prompt_completo):
    try:
        response = model.generate_content(prompt_completo)

        if response.parts:
            return response.text
        else:
            if response.prompt_feedback:
                st.warning(f"O prompt foi bloqueado. Razão: {response.prompt_feedback.block_reason}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        st.caption(f"Categoria: {rating.category}, Probabilidade: {rating.probability}")
            return "A IA não pôde gerar uma resposta para este prompt. Verifique as mensagens acima ou tente reformular seu pedido."
    except Exception as e:
        st.error(f"Erro ao gerar resposta da IA: {str(e)}")
        if hasattr(e, 'message'): # Tenta obter mais detalhes do erro da API do Gemini
            st.error(f"Detalhe da API Gemini: {e.message}")
        return None

# Título do aplicativo
st.title("Recomendador de jogos com IA 🎮")
st.markdown("Preencha com base nos seus gostos em jogos!")


# Entradas do usuário

generos = [
    "Ação", "Arcade e Ritmo", "Hack and Slash", "Luta e Artes Marciais", "Plataformas",
    "Shoot 'em Up", "Tiro em Primeira Pessoa (FPS)", "Tiro em Terceira Pessoa", "Aventura", "Boa Trama", "Casuais",
    "Metroidvania", "Quebra-Cabeça", "RPGs de Aventura", "Romance Visual", "RPG", "JRPGs",
    "RPGs de Aventura", "RPGs de Ação", "RPGs de Estratégia", "RPGs em Grupos", "RPGs em Turnos", "Roguelike",
    "Simulação", "Construção e Automação", "Empregos e Passatempos", "Encontros", "Espaço e Aviação",
    "Rurais e de Fabricação", "Estratégia", "Cidades e Colônias", "Defesa de Torres",
    "Estratégia Baseada em Turnos", "Estratégia em Tempo Real (RTS)", "Militar",
    "Tabuleiro e Cartas", "Corrida", "Esportes","Pescaria e Caça", "Simuladores Automobilísticos"
]
genero_selecionados = st.multiselect(
    "Quais são os gêneros de jogos que voce gosta?",
    generos,
    default=[]
)

temas_opcoes = [
    "Anime", "Espaciais", "Ficção Científica e Cyberpunk", "Mistério e Investigação", "Mundo Aberto",
    "Sobrevivência", "Somente para Adultos", "Terror", "Medieval", "Fantasia"
]
temas_selecionados = st.multiselect(
    "Quais os temas que voce prefere?",
    temas_opcoes,
    default=[]
)



tipo_jogador = st.radio(
    "Qual tipo de Jogadores deseja?",
    ["Qualquer um", "Competitivo On-line", "Cooperativo", "MMO", "Multijogador",
     "Multijogador Local e em Grupo", "Rede Local (LAN)", "Um Jogador"]
)

plataforma_jogo = st.radio(
    "Em qual plataforma deseja jogar o jogo?",
    [ "Qualquer uma", "Pc", "Xbox", "Playstation", "Nintendo"]
)

jogo_duracao = st.selectbox(
    "Qual duração dos jogos que deseja?",
    ["Ate 10h", "Ate 30h", "Ate 50h", "Ate 100h", "Mais de 100h"]
)

valor = st.slider("Qual o valor dos jogos que deseja?", 0, 500, 250)

jogos_jogados = st.text_area(
    "Cite jogos que voce ja jogou e que lhe agradaram:",
    placeholder="Ex: God of war, Elden Ring, Mario, Fortnite, Gta, Call of Duty..."
)

if st.button("Gerar Sugestão de Roteiro"):
    if not generos:
        st.warning("Por favor, informe o destino da viagem.")
    else:


        prompt_aluno = (
            f"Preciso de ajuda para Descobrir jogos para jogar com intuito de lazer.\n"
            f"Os Generos que mais gosto são: {genero_selecionados}.\n"
            f"Os temas que me interessam são:: {temas_selecionados}.\n"
            f"Os tipos de jogador(um jogador, online, etc..) que quero é: '{tipo_jogador}'.\n"
            f"Minha plataforma de preferencia é: '{plataforma_jogo}'.\n"
            f"A duração do jogo que eu quero é de: '{jogo_duracao}'.\n"
            f"O valor que eu posso arcar com o jogo é de até: '{valor}'.\n"
            f"Jogos que ja joguei e gostei como referencia: '{jogos_jogados if jogos_jogados else 'Não joguei nenhum jogo.'}'\n\n"
            f"Com base nessas informações, sugira uma lista de jogos, mostrando os generos de cada jogo, as pkataformas em que ele esta disponivel,"
            f"Os tipos de jogadores, O valor do jogos, e uma descrição sobre os jogos "

        )

        st.markdown("---")
        st.markdown("⚙️ **Prompt que será enviado para a IA (para fins de aprendizado):**")
        st.text_area("",prompt_aluno, height=250)
        st.markdown("---")

        st.info("Aguarde, a IA está escolhendo os melhores jogos para voce!")
        resposta_ia = gerar_resposta_gemini(prompt_aluno)

        if resposta_ia:
            st.markdown("### 🕹Jogos sugeridos:")
            st.markdown(resposta_ia)
        else:
            st.error("Não foi possível gerar o roteiro. Verifique as mensagens acima ou tente novamente mais tarde.")