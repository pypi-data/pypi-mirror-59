Multicoder
==========

Ever asked yourself which encoding returns "Il+n%27y+a+personne+qui+n%27aime+la+souffrance+pour+elle-m%C3%AAme%2C+qui+ne+la+recherche+et+qui+ne+la+veuille+pour+elle-m%C3%AAme%E2%80%A6"?
Multicoder to the rescue!

Multicoder will encode, or decode, the given text using the standard encodings.

```bash
>> pip3 install multicoder
>> multicoder -r "Il+n%27y+a+personne+qui+n%27aime+la+souffrance+pour+elle-m%C3%AAme%2C+qui+ne+la+recherche+et+qui+ne+la+veuille+pour+elle-m%C3%AAme%E2%80%A6"
email.header.decode_header : Il+n%27y+a+personne+qui+n%27aime+la+souffrance+pour+elle-m%C3%AAme%2C+qui+ne+la+recherche+et+qui+ne+la+veuille+pour+elle-m%C3%AAme%E2%80%A6
quopri.decodestring : Il+n%27y+a+personne+qui+n%27aime+la+souffrance+pour+elle-m%C3%AAme%2C+qui+ne+la+recherche+et+qui+ne+la+veuille+pour+elle-m%C3%AAme%E2%80%A6
urllib.parse.unquote : Il+n'y+a+personne+qui+n'aime+la+souffrance+pour+elle-même,+qui+ne+la+recherche+et+qui+ne+la+veuille+pour+elle-même…
urllib.parse.unquote_plus : Il n'y a personne qui n'aime la souffrance pour elle-même, qui ne la recherche et qui ne la veuille pour elle-même…
html.unescape : Il+n%27y+a+personne+qui+n%27aime+la+souffrance+pour+elle-m%C3%AAme%2C+qui+ne+la+recherche+et+qui+ne+la+veuille+pour+elle-m%C3%AAme%E2%80%A6
base64.b64encode : (invalid: Incorrect padding )
base64.urlsafe_b64encode : (invalid: Invalid base64-encoded string: number of data characters (129) cannot be 1 more than a multiple of 4 )
```

You can encode or decode the provided text (of course, some methods can only encode since they are actuall hash methods, not encoding methods…):
```bash
>> multicoder  "Il n'y a personne qui n'aime la souffrance pour elle-même, qui ne la recherche et qui ne la veuille pour elle-même…"
quopri.encodestring : Il n'y a personne qui n'aime la souffrance pour elle-m=C3=AAme, qui ne la r=
echerche et qui ne la veuille pour elle-m=C3=AAme=E2=80=A6
urllib.parse.quote : Il%20n%27y%20a%20personne%20qui%20n%27aime%20la%20souffrance%20pour%20elle-m%C3%AAme%2C%20qui%20ne%20la%20recherche%20et%20qui%20ne%20la%20veuille%20pour%20elle-m%C3%AAme%E2%80%A6
urllib.parse.quote_plus : Il+n%27y+a+personne+qui+n%27aime+la+souffrance+pour+elle-m%C3%AAme%2C+qui+ne+la+recherche+et+qui+ne+la+veuille+pour+elle-m%C3%AAme%E2%80%A6
html.escape : Il n&#x27;y a personne qui n&#x27;aime la souffrance pour elle-même, qui ne la recherche et qui ne la veuille pour elle-même…
shlex.quote : 'Il n'"'"'y a personne qui n'"'"'aime la souffrance pour elle-même, qui ne la recherche et qui ne la veuille pour elle-même…'
base64.b64encode : SWwgbid5IGEgcGVyc29ubmUgcXVpIG4nYWltZSBsYSBzb3VmZnJhbmNlIHBvdXIgZWxsZS1tw6ptZSwgcXVpIG5lIGxhIHJlY2hlcmNoZSBldCBxdWkgbmUgbGEgdmV1aWxsZSBwb3VyIGVsbGUtbcOqbWXigKY=
base64.urlsafe_b64encode : SWwgbid5IGEgcGVyc29ubmUgcXVpIG4nYWltZSBsYSBzb3VmZnJhbmNlIHBvdXIgZWxsZS1tw6ptZSwgcXVpIG5lIGxhIHJlY2hlcmNoZSBldCBxdWkgbmUgbGEgdmV1aWxsZSBwb3VyIGVsbGUtbcOqbWXigKY=
base64.b32encode : JFWCA3RHPEQGCIDQMVZHG33ONZSSA4LVNEQG4J3BNFWWKIDMMEQHG33VMZTHEYLOMNSSA4DPOVZCAZLMNRSS23ODVJWWKLBAOF2WSIDOMUQGYYJAOJSWG2DFOJRWQZJAMV2CA4LVNEQG4ZJANRQSA5TFOVUWY3DFEBYG65LSEBSWY3DFFVW4HKTNMXRIBJQ=
base64.b16encode : 496C206E2779206120706572736F6E6E6520717569206E2761696D65206C6120736F75666672616E636520706F757220656C6C652D6DC3AA6D652C20717569206E65206C612072656368657263686520657420717569206E65206C6120766575696C6C6520706F757220656C6C652D6DC3AA6D65E280A6
base64.a85encode : 8SfMe-[?hC+E1n4F)Pr6AKYu8Bcq:@@;0Ri+DbI/F)Q25Ao_<t@q?d%Dfp(CASc0o/T&D*D.P7@EHPt<DIjr,@3BT%@q]Fo@q]ErATT&7F_Mt9AKYet+Eh==Bl%Ts+E27AEZeq0Ch528_l@Qbiddm
base64.b85encode : No*i)CwU-YAaG@Jb8l{LWgu~NX&`PVVQFn;AZ%eEb8mHKW^!R}V`U(4Z*_7YWo&F^Ep5Z9ZDlMVadl}RZe<{BVIXp4V`yb^V`ya{Wpp5Mb!i}OWgu)}Aa-SSX>4p|AaHMWav)`FY-KHN!>Vm%;((?
hashlib.blake2b : 14e116c68ed87cba179594b29be8c0a91d88770e66e6cc2c7ff4eddbb952d65089bc1393b0c6d7d368db5055e5ede403ccc03d07f89ef9eaf0017eb87e1fd98a
hashlib.blake2s : 2719adfe1e2d364758209952e7dfbe654f8e13167e80835b2537e3acf919e9d5
hashlib.md5 : 1411736ba7c9940e0f659cefebbfa5e3
hashlib.sha1 : d15f196d4ae9eda069d1ea171a44aaa602d581ab
hashlib.sha224 : 0091a239c82042505b10e6c3e286d7f38bdb928fd216f5cfec62298e
hashlib.sha256 : 4c94a96af5fbf5a488a98f26878b9b2f5de3d1aedbe050a4905bae7a7195818c
hashlib.sha384 : 02489c0229904a7e8ec7eb237ce7f9247aaa0b583d61707f387a1ae75dd3bc16d2ffce00df385d636c1c4eb7ec98df42
hashlib.sha3_224 : caa79a4a7278161708481a351194db9f51442cf1f46f1f441c1514b7
hashlib.sha3_256 : 79f093adfc77222a202d4f0985797f5eed214efed8f2f14d87967c98c83a5413
hashlib.sha3_384 : e132d39e20930b6f36021fa0674742cc772b36b44f5ad0c2818581e56596846967cf07c8320f72468989ba0ab7e0b397
hashlib.sha3_512 : 06ce9f1993ef7ff75af589621319a1e5e5bef34a9652728223b9c30d327c1cbcbbd63d3edd6f0b988b48be5be17b9f38fdc95bc4d083d996d399c90f1f1c315a
hashlib.sha512 : 221b768a20c6b1cbc1df7de4fc1724f61b5f2442b8ca325db3f0333b2bb012eaefa731fea951fa5d731b3597f7aa2dc76189bda4be28a9b331546f4a68332897
```

If you known both clear and encoded text, you can display valid encodings:
```bash
>> multicoder "Il n'y a personne qui n'aime la souffrance pour elle-même, qui ne la recherche et qui ne la veuille pour elle-même…" --output d15f196d4ae9eda069d1ea171a44aaa602d581ab
hashlib.sha1 : d15f196d4ae9eda069d1ea171a44aaa602d581ab
```

Probably not the script of the decade but it can help.