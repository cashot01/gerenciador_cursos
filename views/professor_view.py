from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import IntPrompt, Prompt, Confirm

from models.professor import Professor
from services.gerenciador import GerenciadorCursos

console = Console()

def voltar_ao_menu():
    Prompt.ask("\n[dim]Pressione Enter para continuar[/dim]")

def menu_professores(professores: list[Professor]) -> int:
    console.print(Panel("[bold blue]👨‍🏫 Gerenciar Professores[/bold blue]", border_style="blue"))
    opcoes = [
        "1. ➕ Cadastrar Novo Professor",
        "2. 👁️ Listar Todos os Professores",
        "3. ✏️ Editar Professor",
        "4. 🗑️ Excluir Professor",
        "5. 🔙 Voltar ao Menu Principal"
    ]
    for op in opcoes:
        console.print(f"  • {op}")
    return IntPrompt.ask("\n[bold green]Escolha uma opção[/bold green]", default=5)

def criar_professor() -> Professor | None:
    console.print(Panel("➕ [bold]Novo Professor[/bold]", border_style="blue"))
    nome = Prompt.ask("  Nome")
    email = Prompt.ask("  Email")
    especialidade = Prompt.ask("  Especialidade")
    try:
        prof = Professor(nome, email, especialidade)
        GerenciadorCursos.adicionar_professor(prof)
        console.print(f"  ✅ [green]Professor '{prof.nome}' cadastrado![/green]")
        return prof
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")
        return None

def listar_professores():
    console.print(Panel("👁️ [bold]Professores Cadastrados[/bold]", border_style="blue"))
    professores = GerenciadorCursos.listar_professores()
    if not professores:
        console.print("  📭 [dim]Nenhum professor cadastrado.[/dim]")
        return
    table = Table(show_header=True, header_style="bold blue", show_lines=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Nome")
    table.add_column("Email")
    table.add_column("Especialidade")
    for i, p in enumerate(professores, 1):
        table.add_row(str(i), p.nome, p.email, p.especialidade)
    console.print(table)

def editar_professor():
    professores = GerenciadorCursos.listar_professores()
    if not professores:
        console.print("  ⚠️ [yellow]Nenhum professor cadastrado.[/yellow]")
        return
    listar_professores()
    idx = IntPrompt.ask("  Selecione o professor para editar", default=1) - 1
    if not (0 <= idx < len(professores)):
        console.print("  ❌ [red]Professor inválido[/red]")
        return
    prof_antigo = professores[idx]
    console.print(Panel(f"✏️ [bold]Editar: {prof_antigo.nome}[/bold]", border_style="yellow"))
    novo_nome = Prompt.ask("  Nome", default=prof_antigo.nome)
    novo_email = Prompt.ask("  Email", default=prof_antigo.email)
    nova_especialidade = Prompt.ask("  Especialidade", default=prof_antigo.especialidade)
    try:
        novo_prof = Professor(novo_nome, novo_email, nova_especialidade)
        GerenciadorCursos.editar_professor(prof_antigo.email, novo_prof)
        console.print(f"  ✅ [green]Professor atualizado com sucesso![/green]")
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")

def excluir_professor():
    professores = GerenciadorCursos.listar_professores()
    cursos = GerenciadorCursos._cursos
    if not professores:
        console.print("  ⚠️ [yellow]Nenhum professor cadastrado.[/yellow]")
        return
    listar_professores()
    idx = IntPrompt.ask("  Selecione o professor para excluir", default=1) - 1
    if not (0 <= idx < len(professores)):
        console.print("  ❌ [red]Professor inválido[/red]")
        return
    prof = professores[idx]
    cursos_vinculados = [c for c in cursos if c.professor.email == prof.email]
    if cursos_vinculados:
        console.print(f"  ⚠️ [yellow]Professor possui {len(cursos_vinculados)} curso(s) vinculado(s).[/yellow]")
        for c in cursos_vinculados:
            console.print(f"     - {c.codigo}: {c.nome}")
        if not Confirm.ask("  Deseja excluir mesmo assim? (cursos ficarão sem professor)"):
            console.print("  ⚪ [dim]Operação cancelada.[/dim]")
            return
    if Confirm.ask(f"  Confirmar exclusão de [red]{prof.nome}[/red]?"):
        GerenciadorCursos.excluir_professor(prof.email)
        console.print(f"  ✅ [green]Professor excluído com sucesso![/green]")
    else:
        console.print("  ⚪ [dim]Operação cancelada.[/dim]")

def gerenciar_professores():
    """Loop principal do menu de professores."""
    while True:
        from main import limpar_tela  # Import aqui para evitar circular
        limpar_tela()
        professores = GerenciadorCursos.listar_professores()
        sub_opcao = menu_professores(professores)
        
        if sub_opcao == 1:
            criar_professor()
        elif sub_opcao == 2:
            listar_professores()
        elif sub_opcao == 3:
            editar_professor()
        elif sub_opcao == 4:
            excluir_professor()
        elif sub_opcao == 5:
            break
        voltar_ao_menu()