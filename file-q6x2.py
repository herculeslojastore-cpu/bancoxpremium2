import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv("BOT_TOKEN")

# --- DADOS DOS PRODUTOS (EXPANDIDOS PARA ATENDER AOS PEDIDOS) ---
produtos = {
    "itaum": {
        "titulo": "Itaú Consultável",
        "descricao": "Acesso total ao App do Itaú. Saldo visível.",
        "qtd": 10,
        "itens": [
            {"saldo": "R$ 1.500,00", "preco": "R$ 600,00", "id": 1},
            {"saldo": "R$ 2.000,00", "preco": "R$ 850,00", "id": 2},
            {"saldo": "R$ 3.500,00", "preco": "R$ 1.200,00", "id": 3},
            {"saldo": "R$ 4.000,00", "preco": "R$ 1.500,00", "id": 4},
            {"saldo": "R$ 5.000,00", "preco": "R$ 1.800,00", "id": 5},
            {"saldo": "R$ 6.000,00", "preco": "R$ 2.100,00", "id": 6},
            {"saldo": "R$ 7.500,00", "preco": "R$ 2.500,00", "id": 7},
            {"saldo": "R$ 8.200,00", "preco": "R$ 2.800,00", "id": 8},
            {"saldo": "R$ 9.000,00", "preco": "R$ 3.100,00", "id": 9},
            {"saldo": "R$ 10.000,00", "preco": "R$ 3.500,00", "id": 10},
        ]
    },
    "porto": {
        "titulo": "Porto Consultado",
        "descricao": "Saldo garantido (Consultado no telefone).",
        "qtd": 7,
        "itens": [
            {"saldo": "R$ 3.000,00", "preco": "R$ 1.200,00", "id": 1},
            {"saldo": "R$ 3.500,00", "preco": "R$ 1.400,00", "id": 2},
            {"saldo": "R$ 4.000,00", "preco": "R$ 1.600,00", "id": 3},
            {"saldo": "R$ 5.000,00", "preco": "R$ 2.000,00", "id": 4},
            {"saldo": "R$ 6.000,00", "preco": "R$ 2.400,00", "id": 5},
            {"saldo": "R$ 8.000,00", "preco": "R$ 3.200,00", "id": 6},
            {"saldo": "R$ 10.000,00", "preco": "R$ 4.000,00", "id": 7},
        ]
    },
    "lara": {
        "titulo": "Lara (Mercado Pago PJ)",
        "descricao": "Conta PJ pronta para receber via link.",
        "qtd": 21,
        "itens": [
            {"saldo": "R$ 5.000,00", "preco": "R$ 2.000,00", "id": 1},
            {"saldo": "R$ 10.000,00", "preco": "R$ 4.000,00", "id": 2},
            {"saldo": "R$ 15.000,00", "preco": "R$ 6.000,00", "id": 3},
            # Adicione mais itens conforme necessário
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

# --- HISTÓRICO DE COMPRAS (DICIONÁRIO EM MEMÓRIA) ---
# Estrutura: { user_id: [ {produto: ..., item: ..., id: ...}, ... ] }
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
    await update.callback_query.edit_message_text(
        "🏦 **BANCO X PREMIUM**\n"
        "Estoque exclusivo e acesso direto ao sistema. Selecione uma opção:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def menu_comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏦 Itaú (10 vagas)", callback_data='menu_cat_itaum')],
        [InlineKeyboardButton("💳 Porto (7 vagas)", callback_data='menu_cat_porto')],
        [InlineKeyboardButton("💰 Lara (21 vagas)", callback_data='menu_cat_lara')],
        [InlineKeyboardButton("🔐 Logins Premium (50)", callback_data='menu_cat_logins')],
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
        "1️⃣ **Estoque Limitado:** As vagas são liberadas com urgência. Quem demora, perde.\n"
        "2️⃣ **Pagamento:** Somente via Carteira Telegram para garantia de entrega.\n"
        "3️⃣ **Entrega:** Os dados são enviados via Telegram imediatamente após a confirmação do Pix.\n"
        "4️⃣ **Suporte:** Bruno está disponível 24/7 no grupo VIP.\n"
        "5️⃣ **Não reembolso:** Produtos digitais não possuem devolução.\n\n"
        "Ao comprar, você concorda com estas regras."
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
        text += "\n*Acesse o menu Comprar para novos pedidos.*
    
    keyboard = [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data='menu_principal')]]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def menu_suporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("👤 **SOLICITAR SUPORTE**\n\nBruno está no grupo VIP.\nEntre no grupo agora mesmo para ser atendido.")

# --- LÓGICA DE PRODUTOS (PAGINAÇÃO) ---

async def show_cat_produtos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    cat = query.data.split('_')[2] # itaum, porto, lara
    
    p = produtos[cat]
    text = f"🏦 **{p['titulo']}** ({p['qtd']} vagas)\n*{p['descricao']}*\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Voltar para Comprar", callback_data='menu_comprar')]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_prod_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    cat = query.data.split('_')[2]
    page = int(query.data.split('_')[3])
    
    p = produtos[cat]
    items = p['itens']
    items_per_page = 2
    total_pages = (len(items) + items_per_page - 1) // items_per_page
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_items = items[start_idx:end_idx]
    
    text = f"🏦 **{p['titulo']}** - Página {page}/{total_pages}\n\n"
    
    for item in current_items:
        text += f"🔹 Saldo: **{item['saldo']}**\n"
        text += f"🔸 Preço: **{item['preco']}**\n"
        text += f"🔒 ID: {item['id']}\n\n"
        
        # Botão de Comprar na lista
        text += f"🛒 [Comprar {item['saldo']}]({query.url})" # Nota: query.url não funciona em callback, vamos usar botão
    
    keyboard = [
        [InlineKeyboardButton("🔙 Voltar para Comprar", callback_data='menu_comprar')]
    ]
    
    # Adicionar Navegação
    if page > 1:
        keyboard[0].append(InlineKeyboardButton("⬅️ Anterior", callback_data=f'page_{cat}_{page-1}'))
    if page < total_pages:
        keyboard[0].append(InlineKeyboardButton("Próximo ➡️", callback_data=f'page_{cat}_{page+1}'))
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def buy_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    cat = query.data.split('_')[2]
    item_id = int(query.data.split('_')[3])
    
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
        
        text = (
            f"✅ **PEDIDO CONFIRMADO!**\n\n"
            f"Você comprou o **{p['titulo']}** com saldo de **{item['saldo']}**.\n"
            f"Preço: R$ {item['preco']}\n\n"
            f"👉 **AGORA PAGUE PELO TELEGRAM:**\n"
        )
        
        keyboard = [
            [InlineKeyboardButton("💰 Ver Pagamento", callback_data='menu_pagamento')],
            [InlineKeyboardButton("🔙 Menu Principal", callback_data='menu_principal')]
        ]
        
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# --- LÓGICA DE LOGINS (TODOS BOTÕES) ---

async def show_logins_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🔐 **LOGINS PREMIUM (50 Vagas)**\n*Escolha a loja/loja que você quer comprar*\n\n"
    
    keyboard = []
    row = []
    count = 0
    
    for cat, lojas in logins.items():
        for loja in lojas:
            row.append(InlineKeyboardButton(f"🔹 {loja}", callback_data=f'buy_login_{loja}'))
            count += 1
            
            if len(row) == 3: # 3 botões por linha
                keyboard.append(row)
                row = []
    
    if row: keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Voltar para Comprar", callback_data='menu_comprar')])
    
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

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
    
    text = f"✅ **PEDIDO CONFIRMADO!**\n\nVocê selecionou o login da **{loja}**.\n👉 Pague via Telegram Wallet e Bruno liberará o acesso."
    
    keyboard = [
        [InlineKeyboardButton("💰 Ver Pagamento", callback_data='menu_pagamento')],
        [InlineKeyboardButton("🔙 Menu Principal", callback_data='menu_principal')]
    ]
    
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# --- PAGAMENTO ---

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
    
    # PRODUTOS (CATEGORIAS)
    elif data == 'menu_cat_itaum':
        await show_cat_produtos(update, context)
    elif data == 'menu_cat_porto':
        await show_cat_produtos(update, context)
    elif data == 'menu_cat_lara':
        await show_cat_produtos(update, context)
    elif data == 'menu_cat_logins':
        await show_logins_list(update, context)
    
    # PRODUTOS (PÁGINAS)
    elif data.startswith('page_'):
        await show_prod_item(update, context)
    
    # COMPRAR ITENS
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