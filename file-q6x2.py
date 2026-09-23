import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv("BOT_TOKEN")

# --- DADOS DOS PRODUTOS ---
produtos = {
    "itaum": {
        "titulo": "Itaú Consultável",
        "descricao": "Acesso total ao App do Itaú. Saldo visível.",
        "qtd": 10,
        "itens": [
            {"saldo": "R$ 1.500,00", "preco": "R$ 600,00"},
            {"saldo": "R$ 2.000,00", "preco": "R$ 850,00"},
            # Adicione mais itens conforme necessário
        ]
    },
    "porto": {
        "titulo": "Porto Consultado",
        "descricao": "Saldo garantido (Consultado no telefone).",
        "qtd": 7,
        "itens": [
            {"saldo": "R$ 3.000,00", "preco": "R$ 1.200,00"},
            {"saldo": "R$ 5.000,00", "preco": "R$ 2.000,00"},
        ]
    },
    "lara": {
        "titulo": "Lara (Mercado Pago PJ)",
        "descricao": "Conta PJ pronta para receber via link.",
        "qtd": 21,
        "itens": [
            {"saldo": "R$ 10.000,00", "preco": "R$ 4.500,00"},
            {"saldo": "R$ 15.000,00", "preco": "R$ 6.500,00"},
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

# --- DADOS DO PAGAMENTO ---
pagamento = {
    "chave": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh", # Exemplo de chave
    "passo_a_passo": (
        "1. Abra sua carteira Bitcoin (Ex: Binance, Mercado Bitcoin).\n"
        "2. Clique em 'Enviar'.\n"
        "3. Cole a Chave acima.\n"
        "4. Digite a quantidade em R$.\n"
        "5. Confirme a transferência."
    )
}

# --- PAGANDO PELO TELEGRAM (MAIS FÁCIL) ---
pagamento = {
    "chave": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh", # Exemplo de chave
    "pague pelo telegram": (
        "1. Procure por '@wallet'.\n"
        "2. Clique em Iniciar (Start) e abra a carteira (Open Wallet).\n"
        "3. Clique em Comprar criptomoeda (Top up / Buy crypto).\n"
        "4. Selecione a moeda que deseja adquirir (Bitcoin).\n"
        "5. Escolha o método de pagamento Pix.\n"
        "6. Insira o valor em Reais (BRL).\n"
        "7. Informe os dados solicitados.\n"
        "8. Copie o código Pix Copia e Cola e faça o pagamento.\n"
        "9. Aguarde alguns minutos para a compensação.\n"
        "10. Ainda na carteira selecione Enviar ou Sacar.\n"
        "11. Escolha o método de envio (endereço externo de carteira).\n"
        "12. Cole o endereço da carteira acima.\n"
        "13. Insira o valor, confira e confirme."
    )
}

# --- FUNÇÕES ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # MENU PRINCIPAL
    keyboard = [
        [InlineKeyboardButton("🏦 Itaú (10 vagas)", callback_data='menu_itaum')],
        [InlineKeyboardButton("💳 Porto (7 vagas)", callback_data='menu_porto')],
        [InlineKeyboardButton("💰 Lara (21 vagas)", callback_data='menu_lara')],
        [InlineKeyboardButton("🔐 Logins Premium (50)", callback_data='menu_logins')],
        [InlineKeyboardButton("₿ Pagamento Bitcoin", callback_data='menu_pagamento')],
        [InlineKeyboardButton("👤 Suporte VIP (Bruno)", callback_data='menu_suporte')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏦 **BANCO X PREMIUM**\n"
        "Estoque exclusivo e acesso direto ao sistema. Escolha uma opção abaixo:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# --- LÓGICA DOS MENUS ---

async def show_itaum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p = produtos["itaum"]
    text = f"🏦 **{p['titulo']}** ({p['qtd']} vagas)\n*{p['descricao']}*\n\n"
    
    for item in p['itens']:
        text += f"🔹 Saldo: **{item['saldo']}**\n"
        text += f"🔸 Preço: **{item['preco']}**\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='start')],
        [InlineKeyboardButton("🔐 Bloquear este item", callback_data=f'bloquear_itaum')]
    ]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_porto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p = produtos["porto"]
    text = f"💳 **{p['titulo']}** ({p['qtd']} vagas)\n*{p['descricao']}*\n\n"
    for item in p['itens']:
        text += f"🔹 Saldo: **{item['saldo']}**\n"
        text += f"🔸 Preço: **{item['preco']}**\n\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='start')]]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_lara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p = produtos["lara"]
    text = f"💰 **{p['titulo']}** ({p['qtd']} vagas)\n*{p['descricao']}*\n\n"
    for item in p['itens']:
        text += f"🔹 Saldo: **{item['saldo']}**\n"
        text += f"🔸 Preço: **{item['preco']}**\n\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='start')]]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_logins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🔐 **LOGINS PREMIUM (50 Vagas)**\n*Lojas que todos querem comprar*\n\n"
    
    # Cria botões para cada categoria para não poluir a tela
    keyboard = []
    for cat, lojas in logins.items():
        # Limita a 3 itens por botão para ficar organizado
        text_preview = ", ".join(lojas[:3]) 
        if len(lojas) > 3: text_preview += "..."
        
        keyboard.append([InlineKeyboardButton(f"📂 {cat.title()} ({len(lojas)})", callback_data=f'cat_{cat}')])

    keyboard.append([InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='start')])
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_login_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')[1] # Pega 'ecommerce', 'moda', etc
    
    lojas = logins.get(data, [])
    text = f"📂 **CATEGORIA: {data.title()}**\n\n"
    
    for loja in lojas:
        text += f"🔹 {loja}\n"
        
    keyboard = [[InlineKeyboardButton("🔙 Voltar aos Logins", callback_data='menu_logins')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"₿ **PAGAMENTO VIA BITCOIN**\n\n"
    text += f"🔑 **CHAVE:***\n`{pagamento['chave']}`\n\n"
    text += f"📝 **PASSO A PASSO:***\n`{pagamento['passo_a_passo']}`\n\n"
    text += "⚠️ **IMPORTANTE:**\nApós transferir, clique no botão abaixo para enviar o comprovante para o Bruno."
    
    keyboard = [
        [InlineKeyboardButton("✅ Enviar Comprovante para Bruno", callback_data='pedir_para_bruno')],
        [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='start')]
    ]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def pedir_para_bruno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Em um bot real, você enviaria o chat do Bruno aqui.
    # A mensagem diz ao usuário para enviar o comprovante e encaminhar para Bruno.
    text = (
        "✅ **PEDIDO ENVIADO AO BRUNO**\n\n"
        "Bruno está online. Por favor:\n"
        "1. Envie o comprovante de transferência aqui neste chat.\n"
        "2. Bruno já vai receber e liberar seu acesso imediatamente."
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='start')]]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def suporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("👤 **SOLICITAR SUPORTE**\n\n"
    "Bruno está no grupo VIP.\n"
    "Entrar no grupo agora mesmo para ser atendido.")


# --- HANDLERS GERAIS ---

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Confirma clique

    data = query.data

    if data == 'start':
        await start(update, context)
    
    elif data == 'menu_itaum':
        await show_itaum(update, context)
    
    elif data == 'menu_porto':
        await show_porto(update, context)
    
    elif data == 'menu_lara':
        await show_lara(update, context)
    
    elif data == 'menu_logins':
        await show_logins(update, context)
    
    elif data.startswith('cat_'):
        await show_login_category(update, context)
        
    elif data == 'menu_pagamento':
        await show_pagamento(update, context)
        
    elif data == 'pedir_para_bruno':
        await pedir_para_bruno(update, context)
        
    elif data == 'menu_suporte':
        await suporte(update, context)


if __name__ == '__main__':
    print("🚀 Banco X Premium - Bot Rodando...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()