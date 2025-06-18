from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


class Cryptographer:
    def __init__(self):
        # Расширенный словарь шифрования
        self.codes = {
            'А': 'Ψ', 'а': 'δ', 'Б': 'Θ', 'б': 'ξ', 'В': 'Π', 'в': 'ζ',
            'Г': 'Σ', 'г': 'η', 'Д': 'Φ', 'д': 'υ', 'Е': 'Ω', 'е': 'χ',
            'Ё': 'Λ', 'ё': 'ψ', 'Ж': 'Γ', 'ж': 'ω', 'З': 'Δ', 'з': 'ά',
            'И': 'Ξ', 'и': 'έ', 'Й': 'Ο', 'й': 'ή', 'К': 'Ζ', 'к': 'ί',
            'Л': 'Ϋ', 'л': 'ό', 'М': 'Ϊ', 'м': 'ύ', 'Н': 'Ϙ', 'н': 'ώ',
            'О': 'Ϛ', 'о': 'Ϗ', 'П': 'Ϝ', 'п': 'ϗ', 'Р': 'Ϟ', 'р': 'Ϡ',
            'С': 'Ϣ', 'с': 'Ϥ', 'Т': 'Ϧ', 'т': 'Ϩ', 'У': 'Ϫ', 'у': 'Ϭ',
            'Ф': 'Ϯ', 'ф': 'ϴ', 'Х': 'ϵ', 'х': 'Ϸ', 'Ц': 'Ϲ', 'ц': 'Ͻ',
            'Ч': 'Ͼ', 'ч': 'Ͽ', 'Ш': 'Ѐ', 'ш': 'Ё', 'Щ': 'Ђ', 'щ': 'Ѓ',
            'Ъ': 'Є', 'ъ': 'Ѕ', 'Ы': 'І', 'ы': 'Ї', 'Ь': 'Ј', 'ь': 'Љ',
            'Э': 'Њ', 'э': 'Ћ', 'Ю': 'Ќ', 'ю': 'Ѝ', 'Я': 'Ў', 'я': 'Џ',
            '0': '①', '1': '②', '2': '③', '3': '④', '4': '⑤',
            '5': '⑥', '6': '⑦', '7': '⑧', '8': '⑨', '9': '⑩',
            '!': '⦀', '@': '⦁', '#': '⦂', '$': '⦃', '%': '⦄',
            '^': '⦅', '&': '⦆', '*': '⦇', '(': '⦈', ')': '⦉',
            '-': '⦊', '_': '⦋', '=': '⦌', '+': '⦍', '[': '⦎',
            ']': '⦏', '{': '⦐', '}': '⦑', '|': '⦒', '\\': '⦓',
            ';': '⦔', ':': '⦕', "'": '⦖', '"': '⦗', ',': '⦘',
            '.': '⦙', '<': '⦚', '>': '⦛', '/': '⦜', '?': '⦝',
            '`': '⦞', '~': '⦟', ' ': '␣', '\n': '⏎', '\t': '⇥'
        }

    def encrypt_text(self, text, level=1):
        """Рекурсивное шифрование текста"""
        if level <= 0:
            return text
        encrypted = ''.join([self.codes.get(char, char) for char in text])
        return self.encrypt_text(encrypted, level - 1)

    def decrypt_text(self, text, level=1):
        """Рекурсивное дешифрование текста"""
        if level <= 0:
            return text
        reverse_codes = {v: k for k, v in self.codes.items()}
        decrypted = ''.join([reverse_codes.get(char, char) for char in text])
        return self.decrypt_text(decrypted, level - 1)


cryptographer = Cryptographer()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        text = request.form.get('text', '')
        level = int(request.form.get('level', 1))

        if action == 'encrypt':
            result = cryptographer.encrypt_text(text, level)
            return render_template('index.html',
                                   original_text=text,
                                   result_text=result,
                                   level=level,
                                   action='encrypt')
        elif action == 'decrypt':
            result = cryptographer.decrypt_text(text, level)
            return render_template('index.html',
                                   original_text=text,
                                   result_text=result,
                                   level=level,
                                   action='decrypt')

    return render_template('index.html')


@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    data = request.get_json()
    text = data.get('text', '')
    level = int(data.get('level', 1))
    return jsonify({
        'status': 'success',
        'encrypted_text': cryptographer.encrypt_text(text, level)
    })


@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    data = request.get_json()
    text = data.get('text', '')
    level = int(data.get('level', 1))
    return jsonify({
        'status': 'success',
        'decrypted_text': cryptographer.decrypt_text(text, level)
    })


if __name__ == '__main__':
    app.run(debug=True)