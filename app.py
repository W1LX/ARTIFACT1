from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/order', methods=['POST'])
def handle_order():
    data = request.json
    if not data or 'items' not in data:
        return jsonify({"status": "error", "message": "Данные заказа не получены"}), 400
    
    user = data.get('user', 'Anonymous')
    items = data.get('items', [])
    
    total_price = 0
    for item in items:
        try:
            clean_price = item['price'].replace('$', '').replace(',', '').strip()
            total_price += int(clean_price)
        except (ValueError, KeyError):
            continue

    print("\n" + "=" * 40)
    print(f" [NEW ARCHIVE REQUEST] Собрал: {user}")
    print(f" Всего позиций в запросе: {len(items)}")
    print("-" * 40)
    for index, item in enumerate(items, 1):
        print(f"  {index}. {item.get('title', 'Unknown')} — (${item.get('price', '0')})")
    print("=" * 40)
    print(f" ИТОГОВАЯ СУММА К СДЕЛКЕ: ${total_price}")
    print("=" * 40 + "\n")

    return jsonify({
        "status": "success",
        "message": f"Запрос перехвачен сервером! Добавлено {len(items)} вещей на сумму ${total_price}."
    })

if __name__ == '__main__':
    print("Запуск приватного бэкенд-сервера ARTIFACT [Port: 5000]...")
    app.run(debug=True, port=5000)