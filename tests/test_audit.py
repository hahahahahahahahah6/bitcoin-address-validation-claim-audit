import tempfile
import contextlib
import io
from bitcoin_address_validation_claim_audit.audit import main
import unittest
from pathlib import Path
from bitcoin_address_validation_claim_audit.audit import audit, claims, evidence
from bitcoin_address_validation_claim_audit.phrases import BITCOINADDRESSVALIDATION, NOBITCOINADDRESSVALIDATION, GENERIC_NAMES


class AuditTests(unittest.TestCase):
    def test_phrases(self):
        self.assertEqual((len(set(BITCOINADDRESSVALIDATION)), len(set(NOBITCOINADDRESSVALIDATION)), len(set(GENERIC_NAMES))), (50, 24, 24))
        for phrase in BITCOINADDRESSVALIDATION:
            with self.subTest(phrase=phrase): self.assertEqual(claims(phrase), (True, False))
        for phrase in NOBITCOINADDRESSVALIDATION:
            with self.subTest(phrase=phrase): self.assertEqual(claims(phrase), (False, True))
        self.assertEqual(claims('```\nvalidate bitcoin address\n```'), (False, False))
        self.assertEqual(claims('~~~ text\nvalidate bitcoin address\n~~~'), (False, False))
        self.assertEqual(claims('`validate-bitcoin-address`'), (True, False))
        self.assertEqual(claims("doesn't validate bitcoin address"), (False, True))
        self.assertEqual(claims('validate bitcoin addressXYZ'), (False, False))

    def test_library_routes(self):
        for method in ('validate', 'is_valid'):
            for prefix, call in [('import stdnum.bitcoin', 'stdnum.bitcoin.' + method), ('import stdnum.bitcoin as im', 'im.' + method), ('from stdnum import bitcoin', 'bitcoin.' + method), ('import stdnum', 'stdnum.bitcoin.' + method), ('from stdnum.bitcoin import ' + method, method), ('from stdnum.bitcoin import ' + method + ' as v', 'v')]:
                with self.subTest(method=method, call=call): self.assertTrue(evidence(prefix + '\n' + call + '(x)'))

        for prefix, call in [('import validators', 'validators.btc_address'), ('import validators as v', 'v.btc_address'), ('from validators import crypto_addresses', 'crypto_addresses.btc_address'), ('import validators.crypto_addresses', 'validators.crypto_addresses.btc_address'), ('from validators import btc_address', 'btc_address'), ('from validators.crypto_addresses import btc_address as b', 'b'), ('from validators.crypto_addresses.btc_address import btc_address', 'btc_address')]:
            with self.subTest(call=call): self.assertTrue(evidence(prefix + '\n' + call + '(x)'))

    def test_generic_routes(self):
        for name in GENERIC_NAMES:
            for source in ('obj.' + name + '(x)', 'from lib import ' + name + ' as f\nf(x)', 'obj = factory()\nobj.' + name + '(x)'):
                with self.subTest(source=source): self.assertTrue(evidence(source))

    def test_not_evidence(self):
        cases = ['import stdnum.bitcoin', 'validate(x)', 'is_valid(x)', 'validate_bitcoin_address(x)', 'obj.validate(x)', 'obj.bitcoin_address(x)', 'import stdnum.bitcoin\nstdnum.bitcoin.compact(x)', 'import stdnum.bitcoin\nstdnum.bitcoin.format(x)', 'from stdnum import ean\nean.validate(x)', 'from stdnum import ean\nean.calc_check_digit(x)', 'from stdnum import luhn\nluhn.validate(x)', 'from stdnum import luhn\nluhn.calc_check_digit(x)', 'import re\nre.match(x,y)', 'import re\nre.search(x,y)', 'import re\nre.fullmatch(x,y)', 'len(x) == 12', 'issuer in known', 'validators.bitcoin_address(x)', 'lookup.bitcoin_address(x)', '"validate bitcoin address"', 'validate_bitcoin_address', 'def broken(:', 'import subprocess\nsubprocess.run(["bitcoin_address-check"])', 'import stdnum.bitcoin as im\nim = x\nim.validate(x)', 'from stdnum.bitcoin import validate\nwith x as validate:\n validate(x)', 'def validate_bitcoin_address(x): pass\nobj.validate_bitcoin_address(x)']
        cases += ['bitcoin_address(x)', 'compact(x)', 'format(x)', 'obj.is_valid(x)', 'obj.compact(x)', 'obj.format(x)', 'import validators\nvalidators.bitcoin_address(x)', 'import stdnum.bitcoin as gr\nwith ctx() as gr:\n gr.validate(x)', 'from lib import validate_bitcoin_address as v\nv = other\nv(x)', 'class C:\n def validate_bitcoin_address(self): pass\nobj.validate_bitcoin_address(x)', '# validate bitcoin address\nx = \"bitcoin address validation\"']
        cases += ['from stdnum import ' + n + '\n' + n + '.validate(x)' for n in ('isbn', 'issn', 'ismn', 'isan', 'isin')]
        cases += ['import stdnum.bitcoin\nstdnum.bitcoin.' + x + '(v)' for x in ('compact', 'b58decode', 'b32decode', 'bech32_checksum')]
        cases += ['import validators\nvalidators.' + x + '(v)' for x in ('eth_address', 'bsc_address', 'trx_address')]
        cases += ['v.startswith("bc1")', 'all(c in alphabet for c in v)', 'lookup_address(v)', 'generate_address()', 'validate_transaction(v)', 'validate_payment(v)', 'validate_block(v)', 'validate_wif(v)', 'validate_private_key(v)', 'obj.validate_litecoin_address(v)', 'obj.validate_dogecoin_address(v)']
        for source in cases:
            with self.subTest(source=source): self.assertFalse(evidence(source))

    def test_findings(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); (p/'README.md').write_text('validate bitcoin address')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'tests').mkdir(); (p/'tests/test_a.py').write_text('obj.validate_bitcoin_address(x)')
            self.assertEqual(audit(p)[0]['severity'], 'MEDIUM')
            (p/'a.py').write_text('obj.validate_bitcoin_address(x)')
            self.assertEqual(audit(p), [])
            (p/'README.md').write_text('does not validate bitcoin address')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'a.py').unlink(); self.assertEqual(audit(p), [])
            (p/'README.md').write_text('validate bitcoin address')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['audit', str(p)]), 0)
                self.assertEqual(main(['audit', str(p), '--fail-on', 'medium']), 2)
                self.assertEqual(main(['audit', str(p), '--ignore', 'tests']), 2)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(['audit', str(p/'missing')]), 1)

    def test_exclusions(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); (p/'README.md').write_text('validate bitcoin address')
            for folder in ('fixtures', 'docs', 'examples'):
                (p/folder).mkdir(); (p/folder/'a.py').write_text('obj.validate_bitcoin_address(x)')
            (p/'link.py').symlink_to(p/'fixtures/a.py')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'src.py').write_text('obj.validate_bitcoin_address(x)')
            self.assertEqual(audit(p, ['src.py'])[0]['severity'], 'HIGH')
