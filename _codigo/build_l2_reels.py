from reel_lib import make_reel
B = "/mnt/user-data/uploads/Fotos Star/Anúncio Star/"
print("alexandre", make_reel(B + "Câmbio Automático_/Vídeos_/Star Óleo 1F.MP4",
    [(5.50, 20.06, "COMO FOI O\\NATENDIMENTO?"), (20.16, 32.96, "TUDO CONFORME\\NO COMBINADO?")],
    "out2/reel_depoimento_alexandre.mp4"))
print("lucio", make_reel(B + "Star 1F (feedback).MP4",
    [(6.40, 14.60, "O CARRO CHEGOU\\NBATENDO TUDO"), (16.30, 27.40, "EM OUTRO LUGAR:\\N“É AMORTECEDOR”"), (27.50, 32.60, "E HOJE?\\NCARRO 100%")],
    "out2/reel_depoimento_lucio.mp4"))
print("radiador", make_reel(B + "Star 1F.MP4",
    [(0.0, 5.6, "CAFÉ COM LEITE\\NNO RADIADOR?"), (5.6, 17.0, "ÓLEO MISTURADO\\NCOM A ÁGUA")],
    "out2/reel_dica_radiador.mp4", tag="DICA DO FERNANDO",
    masks=[(14.85, 17.0, 540, 1222, "CHAME A STAR NO WHATSAPP")]))
