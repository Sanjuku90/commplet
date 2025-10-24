"""
Calculateur de profits corrigé pour éviter les erreurs sqlite3.Row
"""

import sqlite3
from datetime import datetime
from sqlite_utils import safe_row_get, row_to_dict

def calculate_daily_profits_safe():
    """
    Version sécurisée du calcul des profits quotidiens
    """
    try:
        conn = sqlite3.connect('investment_platform.db')
        conn.row_factory = sqlite3.Row
        
        # Plus d'investissements ROI actifs
        active_investments = []

        # Récupérer tous les bots de trading actifs
        active_bots = conn.execute('''
            SELECT utb.*, u.email, ts.name as strategy_name
            FROM user_trading_bots utb
            JOIN users u ON utb.user_id = u.id
            JOIN trading_strategies ts ON utb.strategy_id = ts.id
            WHERE utb.is_active = 1
        ''').fetchall()

        # Récupérer tous les copy trades actifs
        active_copies = conn.execute('''
            SELECT uct.*, u.email, tt.name as trader_name, tt.monthly_return
            FROM user_copy_trading uct
            JOIN users u ON uct.user_id = u.id
            JOIN top_traders tt ON uct.trader_id = tt.id
            WHERE uct.is_active = 1
        ''').fetchall()

        print(f"🔄 Calcul des profits pour {len(active_investments)} investissements, {len(active_bots)} bots, {len(active_copies)} copy trades")

        # Traiter les investissements ROI classiques
        for investment in active_investments:
            try:
                # Vérifier si l'investissement est vraiment actif (pas expiré)
                if safe_row_get(investment, 'end_date'):
                    end_date = datetime.fromisoformat(safe_row_get(investment, 'end_date', '').replace('Z', ''))
                    if datetime.now() > end_date:
                        # Marquer comme terminé
                        conn.execute('''
                            UPDATE user_investments 
                            SET is_active = 0 
                            WHERE id = ?
                        ''', (safe_row_get(investment, 'id'),))
                        continue

                # Calculate daily profit
                daily_profit = safe_row_get(investment, 'daily_profit', 0)
                
                if daily_profit > 0:
                    print(f"💰 Ajout de {daily_profit:.2f} USDT pour l'utilisateur {safe_row_get(investment, 'user_id')} - Plan: {safe_row_get(investment, 'plan_name')}")

                    # Update user balance
                    conn.execute('''
                        UPDATE users 
                        SET balance = balance + ? 
                        WHERE id = ?
                    ''', (daily_profit, safe_row_get(investment, 'user_id')))

                    # Update total earned
                    current_earned = safe_row_get(investment, 'total_earned', 0)
                    new_total_earned = current_earned + daily_profit
                    conn.execute('''
                        UPDATE user_investments 
                        SET total_earned = ? 
                        WHERE id = ?
                    ''', (new_total_earned, safe_row_get(investment, 'id')))

            except Exception as e:
                print(f"❌ Erreur calcul profit pour investissement {safe_row_get(investment, 'id', 'unknown')}: {e}")
                continue

        # Traiter les bots de trading
        for bot in active_bots:
            try:
                daily_profit = safe_row_get(bot, 'daily_profit', 0)
                
                if daily_profit > 0:
                    print(f"🤖 Ajout de {daily_profit:.2f} USDT pour le bot {safe_row_get(bot, 'id')} de l'utilisateur {safe_row_get(bot, 'user_id')}")

                    # Mettre à jour le solde utilisateur
                    conn.execute('''
                        UPDATE users 
                        SET balance = balance + ? 
                        WHERE id = ?
                    ''', (daily_profit, safe_row_get(bot, 'user_id')))

                    # Mettre à jour les profits totaux du bot
                    current_profit = safe_row_get(bot, 'total_profit', 0)
                    new_total_profit = current_profit + daily_profit
                    conn.execute('''
                        UPDATE user_trading_bots 
                        SET total_profit = ?, last_profit_date = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    ''', (new_total_profit, safe_row_get(bot, 'id')))

            except Exception as e:
                print(f"❌ Erreur calcul profit pour bot {safe_row_get(bot, 'id', 'unknown')}: {e}")
                continue

        # Traiter les copy trades
        for copy_trade in active_copies:
            try:
                # Calculer le profit basé sur le rendement mensuel du trader
                monthly_return = safe_row_get(copy_trade, 'monthly_return', 0) / 100  # Convertir en décimal
                daily_return = monthly_return / 30  # Approximation quotidienne
                daily_profit = safe_row_get(copy_trade, 'amount', 0) * daily_return * safe_row_get(copy_trade, 'copy_ratio', 1.0)
                
                if daily_profit > 0:
                    print(f"📈 Ajout de {daily_profit:.2f} USDT pour le copy trade {safe_row_get(copy_trade, 'id')} de l'utilisateur {safe_row_get(copy_trade, 'user_id')}")

                    # Mettre à jour le solde utilisateur
                    conn.execute('''
                        UPDATE users 
                        SET balance = balance + ? 
                        WHERE id = ?
                    ''', (daily_profit, safe_row_get(copy_trade, 'user_id')))

                    # Mettre à jour les profits totaux du copy trade
                    current_profit = safe_row_get(copy_trade, 'total_profit', 0)
                    new_total_profit = current_profit + daily_profit
                    conn.execute('''
                        UPDATE user_copy_trading 
                        SET total_profit = ? 
                        WHERE id = ?
                    ''', (new_total_profit, safe_row_get(copy_trade, 'id')))

            except Exception as e:
                print(f"❌ Erreur calcul profit pour copy trade {safe_row_get(copy_trade, 'id', 'unknown')}: {e}")
                continue

        conn.commit()
        conn.close()
        print("✅ Calcul des profits quotidiens terminé")
        
    except Exception as e:
        print(f"❌ Erreur générale calcul profits: {e}")
        if 'conn' in locals():
            conn.close()
