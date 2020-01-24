import sys
sys.path.append('../src')
sys.path.append('../f469-disco/tests')
from pin import Secret, Factory_settings
from platform import storage_root
from unittest import TestCase
import os
from keystore import KeyStore
from bitcoin import bip32, bip39, script

class KeystoreTest(TestCase):

    STORAGE_ROOT = "/tmp/specter_diy_tests"

    def test_create_psbt(self):

        # we need a seed into the keystore
        # convert mnemonic and password to bip-32 seed
        entropy = b'\x64\xd3\xe4\xa0\xa3\x87\xe2\x80\x21\xdf\x55\xa5\x1d\x45\x4d\xcf'
        recovery_phrase = bip39.mnemonic_from_bytes(entropy)
        print("recovery_phrase : "+recovery_phrase)
        
        assert recovery_phrase == "gospel palace choice either lawsuit divorce manual turkey pink tuition fat pair"
        recovery_phrase = "ghost ghost ghost ghost ghost ghost ghost ghost ghost ghost ghost machine"
        seed = bip39.mnemonic_to_seed(recovery_phrase, password="ghost")
        print("seed: " + str(seed))
        keystore = KeyStore(storage_root=self.STORAGE_ROOT)
        keystore.load_seed(seed)
        keystore.load_wallets("regtest")
        keystore.create_wallet("ghost","wpkh([b506aff7/84h/1h/0h]vpub5Y5mzgRhJ3P8oB6t7zCL7Uub1T6f9mgjHN7FeLYztqoj7QhEiXWNz2CWQhavtJJxTwqL2hYgHY46znpnb7neEBg4u6FDy8FdrkcmJdanr3Y)")

        
        #Let's have a transaction:
        # This is mostly copying main.parce_transaction ...

        b64_tx = "cHNidP8BAHECAAAAAZiFAqKtMWL2tVJSKhX04jHxKZvXZg+uPEMD9xdw0PeWAQAAAAD+////AhAnAAAAAAAAFgAUx1fLoej/438ElcbnSI5SmU34AS4DXwEAAAAAABYAFO9bZbq8pL432rtHbfDLPTDgm0FrAAAAAAABAR+ghgEAAAAAABYAFBuVv9WF+yJ2OdWXADeEykvKQpzmIgYCVYCdJLdzBojoCcNiP0OQiaxkArIJnpZFZ7TaCwyub3wYtQav91QAAIABAACAAAAAgAAAAAAAAAAAAAAiAgIhNz1vMGjYOr0S2Vf9bPBXg73ohRv5biNbWsMilIZcBRi1Bq/3VAAAgAEAAIAAAACAAQAAAAAAAAAA"
        from ubinascii import hexlify, unhexlify, a2b_base64, b2a_base64
        raw = a2b_base64(b64_tx)
        from bitcoin import psbt
        tx = psbt.PSBT.parse(raw)
        tx_data = keystore.check_psbt(tx)
        assert tx_data['spending'] == 10141
        assert tx_data['total_in'] == 100000
        assert tx_data['fee'] == 141
        assert tx_data['send_outputs'][0]['value'] == 10000
        assert tx_data['send_outputs'][0]['address'] == "bcrt1qcatuhg0gll3h7py4cmn53rjjn9xlsqfwj3zcej"
