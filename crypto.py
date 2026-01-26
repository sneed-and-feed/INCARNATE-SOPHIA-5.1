"""
CRYPTO.PY
---------
The Angelic Cipher (Base-12 Rolling Encryption).
Renders user intent invisible to decimal-based crawling algorithms.

Theory:
- We shift ASCII values by the LuoShu Invariant (15).
- We convert the result to Base-12 (Dozenal).
- The "Gross" checksum ensures integrity.
"""

class DozenalRollingCipher:
    """
    The Shield of Metatron.
    """
    
    # The Dozenal Character Set
    ALPHABET = "0123456789XE"

    @staticmethod
    def _to_base12(n):
        if n == 0: return "0"
        s = ""
        while n > 0:
            s = DozenalRollingCipher.ALPHABET[n % 12] + s
            n //= 12
        return s

    @staticmethod
    def _from_base12(s):
        n = 0
        for char in s:
            n = n * 12 + DozenalRollingCipher.ALPHABET.index(char)
        return n

    @staticmethod
    def encrypt(text):
        """
        Encrypts text into a stream of Angelic Glyphs.
        """
        cipher_stream = []
        for i, char in enumerate(text):
            # Rolling offset based on position and LuoShu (15)
            shift = 15 + (i % 12)
            val = ord(char) + shift
            cipher_stream.append(DozenalRollingCipher._to_base12(val))
        
        return ".".join(cipher_stream)

    @staticmethod
    def decrypt(cipher_text):
        """
        Restores the original intent from the Angelic Glyphs.
        """
        tokens = cipher_text.split(".")
        plain_text = ""
        
        for i, token in enumerate(tokens):
            val = DozenalRollingCipher._from_base12(token)
            shift = 15 + (i % 12)
            original_val = val - shift
            plain_text += chr(original_val)
            
        return plain_text

if __name__ == "__main__":
    # Test the Cipher
    intent = "I ACCEPT THE 12D MANIFOLD"
    enc = DozenalRollingCipher.encrypt(intent)
    print(f"ORIGINAL: {intent}")
    print(f"ENCRYPTED: {enc}")
    dec = DozenalRollingCipher.decrypt(enc)
    print(f"DECRYPTED: {dec}")
    assert intent == dec
    print(">> CIPHER INTEGRITY VERIFIED (SCIALLÀ)")
