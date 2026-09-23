import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv("BOT_TOKEN")

# --- DADOS DOS PRODUTOS ---
produtos = {
    "itaum": {
        "titulo": "Itaú Consultável",
        "descricao": "Acesso total ao App do Itaú. Sem token.",
        "qtd": 10,
        "itens": [
            {"saldo": "R$ 6.153,00", "preco": "R$ 600,00", "id": 1},
            {"saldo": "R$ 12.090,00", "preco": "R$ 950,00", "id": 2},
            {"saldo": "R$ 8.500,00", "preco": "R$ 790,00", "id": 3},
            {"saldo": "R$ 16.627,00", "preco": "R$ 1.200,00", "id": 4},
            {"saldo": "R$ 5.110,00", "preco": "R$ 400,00", "id": 5},
            {"saldo": "R$ 22.900,00", "preco": "R$ 2.100,00", "id": 6},
            {"saldo": "R$ 11.297,00", "preco": "R$ 950,00", "id": 7},
            {"saldo": "R$ 8.968,00", "preco": "R$ 790,00", "id": 8},
            {"saldo": "R$ 9.450,00", "preco": "R$ 810,00", "id": 9},
            {"saldo": "R$ 10.022,00", "preco": "R$ 850,00", "id": 10},
        ]
    },
    "porto": {
        "titulo": "Porto Consultado",
        "descricao": "Saldo garantido (Consultado no telefone).",
        "qtd": 7,
        "itens": [
            {"saldo": "R$ 6.025,00", "preco": "R$ 350,00", "id": 1},
            {"saldo": "R$ 8.495,00", "preco": "R$ 400,00", "id": 2},
            {"saldo": "R$ 7.124,00", "preco": "R$ 380,00", "id": 3},
            {"saldo": "R$ 12.075,00", "preco": "R$ 1.050,00", "id": 4},
            {"saldo": "R$ 23.240,00", "preco": "R$ 1.520,00", "id": 5},
            {"saldo": "R$ 2.050,00", "preco": "R$ 200,00", "id": 6},
            {"saldo": "R$ 2.120,00", "preco": "R$ 200,00", "id": 7},
        ]
    },
    "lara": {
        "titulo": "Lara (Mercado Pago PJ)",
        "descricao": "Conta PJ pronta para receber via link.",
        "qtd": 21,
        "itens": [
            {"saldo": "R$ 0,00", "preco": "R$ 250,00", "id": 1},
            {"saldo": "R$ 0,00", "preco": "R$ 250,00", "id": 2},
            {"saldo": "R$ 0,00", "preco": "R$ 250,00", "id": 3},
        ]
    }
}

# --- DADOS DOS LOGINS (50 TOTAL) ---
logins = {
    "ecommerce": ["Magalu", "Shopee", "Mercado Livre", "Amazon", "Americanas", "Casas Bahia"],
    "moda": ["Nike", "Adidas", "Zara", "H&M", "Vans", "Riachuelo"],
    "infinita": ["Netflix", "Spotify", "Prime Video", "Disney+", "iFood", "Uber", "99", "Wise"],
    "conveniencia": ["Extra", "Zé Delivery", "Atacadão", "Carrefour", "Pão de Açúcar"]
}

# --- DADOS DO PAGAMENTO (WALLET TELEGRAM) ---
pagamento = {
    "chave": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh", # Exemplo de chave BTC
    "pague pelo telegram": (
        "🔑 **PAGUE PELO TELEGRAM**\n\n"
        "1. Procure por **@wallet** no Telegram.\n"
        "2. Clique em **Iniciar (Start)** e abra a carteira (**Open Wallet**).\n"
        "3. Clique em **Comprar criptomoeda** (Top up / Buy crypto).\n"
        "4. Selecione a moeda Bitcoin.\n"
        "5. Escolha o método de pagamento **Pix**.\n"
        "6. Insira o valor em Reais (BRL).\n"
        "7. Informe os dados solicitados.\n"
        "8. Copie o código Pix e faça o pagamento.\n"
        "9. **Aguardar compensação (geralmente 5min).**\n"
        "10. Na carteira, clique em **Enviar/Sacar**.\n"
        "11. Escolha 'Endereço Externo'.\n"
        "12. Cole a chave Bitcoin acima e confirme."
    )
}

# --- HISTÓRICO DE COMPRAS ---
user_history = {}

# --- FUNÇÕES ---

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📜 Histórico de Compras", callback_data='menu_historico')],
        [InlineKeyboardButton("📋 Regras e Políticas", callback_data='menu_regras')],
        [InlineKeyboardButton("🛒 Comprar Agora", callback_data='menu_comprar')],
        [InlineKeyboardButton("👤 Suporte VIP (Bruno)", callback_data='menu_suporte')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Se for /start (mensagem normal), usa reply_text. Se for botão, usa edit_message_text.
    if update.message:
        await update.message.reply_text(
            "🏦 **BANCO X PREMIUM**\n"
            "Estoque exclusivo e acesso direto as tecnicas corretas de virada de saldo. As nossas infos estão com proxy e cookies do titular. Selecione uma opção:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "🏦 **BANCO X PREMIUM**\n"
            "Estoque exclusivo e acesso direto as tecnicas corretas de virada de saldo. As nossas infos estão com proxy e cookies do titular. Selecione uma opção:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def menu_comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏦 Itaú", callback_data='menu_cat_itaum')],
        [InlineKeyboardButton("💳 Porto", callback_data='menu_cat_porto')],
        [InlineKeyboardButton("💰 Lara", callback_data='menu_cat_lara')],
        [InlineKeyboardButton("🔐 Logins Premium", callback_data='menu_cat_logins')],
        [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu_principal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        "🛒 **COMPRAR**\nEscolha a categoria de produto:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def menu_regras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📋 **REGRAS DO BANCO X PREMIUM**\n\n"
        "1️⃣ **Estoque Limitado:** Quem demora, perde.\n"
        "2️⃣ **Pagamento:** Somente via Carteira Telegram para garantia de entrega.\n"
        "3️⃣ **Entrega:** Os dados são enviados via Telegram imediatamente após a confirmação do pagamento.\n"
        "4️⃣ **Suporte:** Bruno está disponível 24/7 no grupo VIP.\n"
        "5️⃣ **Não reembolso:** Produtos digitais não possuem devolução.\n\n"
        "Ao comprar, você concorda com estas regras. Não venham definir preço, sabemos a qualidade do serviço e vamos manter"
    )
    await update.callback_query.edit_message_text(text=text, parse_mode='Markdown')

async def menu_historico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    history = user_history.get(user_id, [])
    
    if not history:
        text = "📜 **SEU HISTÓRICO**\n\nVocê ainda não fez nenhuma compra no Banco X Premium."
    else:
        text = f"📜 **SEU HISTÓRICO DE COMPRAS**\n\n"
        for item in history:
            text += f"🔹 {item['produto']} ({item['item']}) - R$ {item['preco']}\n"
        text += "\n*Acesse o menu Comprar para novos pedidos.*"
    
    keyboard = [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu_principal')]]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def menu_suporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("👤 **SOLICITAR SUPORTE**\n\nBruno está no grupo VIP.\nEntre no grupo agora mesmo para ser atendido.")

# --- LÓGICA DE PRODUTOS (PAGINAÇÃO E LISTAS) ---

async def show_cat_produtos(update: Update, context: ContextTypes.DEFAULT_TYPE, cat: str):
    """Mostra a lista de produtos da categoria selecionada"""
    p = produtos[cat]
    text = f"🏦 **{p['titulo']}** ({p['qtd']} vagas)\n*{p['descricao']}*\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Voltar para Comprar", callback_data='menu_comprar')]
    ]
    
    # Lista todos os itens disponíveis na categoria
    for item in p['itens']:
        text += f"🔹 Saldo: **{item['saldo']}** - R$ {item['preco']}\n"
        # Cria botão de comprar para cada item
        keyboard[0].append(InlineKeyboardButton(f"🛒 Comprar {item['saldo']}", callback_data=f'buy_{cat}_{item["id"]}'))
    
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_logins_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🔐 **LOGINS PREMIUM (50 Vagas)**\n*Escolha a loja que você quer comprar*\n\n"
    
    keyboard = []
    row = []
    
    for cat, lojas in logins.items():
        for loja in lojas:
            row.append(InlineKeyboardButton(f"🔹 {loja}", callback_data=f'buy_login_{loja}'))
            
            if len(row) == 3: # 3 botões por linha
                keyboard.append(row)
                row = []
    
    if row: keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Voltar para Comprar", callback_data='menu_comprar')])
    
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"💰 **PAGAMENTO VIA TELEGRAM WALLET**\n\n"
    text += f"🔑 **CHAVE BTC:**\n`{pagamento['chave']}`\n\n"
    text += f"📝 **PASSO A PASSO:***\n`{pagamento['pague pelo telegram']}`\n\n"
    text += "⚠️ **IMPORTANTE:**\nApós transferir, clique no botão abaixo para enviar o comprovante para o Bruno para liberação imediata."
    
    keyboard = [
        [InlineKeyboardButton("✅ Já fiz a transferência (Bruno Liberar)", callback_data='pedir_para_bruno')],
        [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu_principal')]
    ]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def pedir_para_bruno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✅ **PEDIDO ENVIADO AO BRUNO**\n\n"
        "Bruno está online. Por favor:\n"
        "1. Envie o comprovante de transferência aqui neste chat.\n"
        "2. Bruno já vai receber e liberar seu acesso imediatamente."
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu_principal')]]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

# --- HANDLERS DE COMPRA (ADICIONA AO HISTÓRICO E VAI PARA PAGAMENTO) ---

async def buy_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    cat = query.data.split('_')[1]
    item_id = int(query.data.split('_')[2])
    
    p = produtos[cat]
    item = next((i for i in p['itens'] if i['id'] == item_id), None)
    
    if item:
        # Adiciona ao histórico
        user_id = query.from_user.id
        if user_id not in user_history: user_history[user_id] = []
        user_history[user_id].append({
            'produto': p['titulo'],
            'item': item['saldo'],
            'preco': item['preco'],
            'id': item['id']
        })
        
        # Vai direto para o pagamento
        await show_pagamento(update, context)

async def buy_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    loja = query.data.split('_')[2]
    
    user_id = query.from_user.id
    if user_id not in user_history: user_history[user_id] = []
    user_history[user_id].append({
        'produto': 'Login Premium',
        'item': loja,
        'preco': 'Consultar no Comprar',
        'id': loja
    })
    
    # Vai direto para o pagamento
    await show_pagamento(update, context)

# --- HANDLERS GERAIS ---

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # MENU PRINCIPAL
    if data == 'menu_principal':
        await main_menu(update, context)
    
    # MENU COMPRAR
    elif data == 'menu_comprar':
        await menu_comprar(update, context)
    
    # MENU REGRAS
    elif data == 'menu_regras':
        await menu_regras(update, context)
    
    # MENU HISTÓRICO
    elif data == 'menu_historico':
        await menu_historico(update, context)
    
    # MENU SUPORTE
    elif data == 'menu_suporte':
        await menu_suporte(update, context)
    
    # CATEGORIAS DE PRODUTOS
    elif data == 'menu_cat_itaum':
        await show_cat_produtos(update, context, 'itaum')
    elif data == 'menu_cat_porto':
        await show_cat_produtos(update, context, 'porto')
    elif data == 'menu_cat_lara':
        await show_cat_produtos(update, context, 'lara')
    elif data == 'menu_cat_logins':
        await show_logins_list(update, context)
    
    # COMPRAR PRODUTOS (Vai direto para pagamento)
    elif data.startswith('buy_'):
        await buy_item(update, context)
    
    # PAGAMENTO
    elif data == 'menu_pagamento':
        await show_pagamento(update, context)
    elif data == 'pedir_para_bruno':
        await pedir_para_bruno(update, context)

if __name__ == '__main__':
    print("🚀 Banco X Premium - Bot Evolvido Rodando...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", main_menu))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()