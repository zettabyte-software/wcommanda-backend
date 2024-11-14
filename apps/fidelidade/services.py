from apps.system.core.classes import Email


def enviar_email_cartao_fidelidade_completo(cartao_fidelidade):
    email = Email(
        titulo="wCommanda | Cartão Fidelidade Completo",
        corpo=(
            "Parabéns! Seu cartão fidelidade foi completo e agora você pode resgatar seu prêmio: "
            f"{cartao_fidelidade.cr_premio.pm_nome}\n"
            f"Clique no link para acessar seu cartão fidelidade virtual: {cartao_fidelidade.cr_link}"
        ),
        destinatarios=[cartao_fidelidade.cr_cliente.cl_email],
    )

    email.send()
