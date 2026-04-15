from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import IntPrompt, Prompt, Confirm

from models.aluno import Aluno
from services.gerenciador import GerenciadorCursos

console = Console()

def voltar_ao_menu():
    Prompt.ask("\n[dim]Pressione Enter para continuar[/dim]")

def menu_alunos(alunos: list[Aluno]) -> int:
    console.print(Panel("[bold green]👨‍🎓 Gerenciar Alunos[/bold green]", border_style="green"))
    opcoes = [
        "1. ➕ Cadastrar Novo Aluno",
        "2. 👁️ Listar Todos os Alunos",
        "3. ✏️ Editar Aluno",
        "4. 🗑️ Excluir Aluno",
        "5. 🔙 Voltar ao Menu Principal"
    ]
    for op in opcoes:
        console.print(f"  • {op}")
    return IntPrompt.ask("\n[bold green]Escolha uma opção[/bold green]", default=5)

def criar_aluno() -> Aluno | None:
    console.print(Panel("➕ [bold]Novo Aluno[/bold]", border_style="green"))
    nome = Prompt.ask("  Nome")
    email = Prompt.ask("  Email")
    try:
        aluno = Aluno(nome, email)
        GerenciadorCursos.adicionar_aluno(aluno)
        console.print(f"  ✅ [green]Aluno '{aluno.nome}' cadastrado! Matrícula: [bold]{aluno.matricula}[/bold][/green]")
        return aluno
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")
        return None

def listar_alunos():
    console.print(Panel("👁️ [bold]Alunos Cadastrados[/bold]", border_style="green"))
    alunos = GerenciadorCursos.listar_alunos()
    if not alunos:
        console.print("  📭 [dim]Nenhum aluno cadastrado.[/dim]")
        return
    table = Table(show_header=True, header_style="bold green", show_lines=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Matrícula", style="cyan")
    table.add_column("Nome")
    table.add_column("Email")
    table.add_column("Média", justify="right")
    for i, a in enumerate(alunos, 1):
        table.add_row(str(i), a.matricula, a.nome, a.email, f"{a.calcular_media():.1f}")
    console.print(table)

def editar_aluno():
    alunos = GerenciadorCursos.listar_alunos()
    if not alunos:
        console.print("  ⚠️ [yellow]Nenhum aluno cadastrado.[/yellow]")
        return
    listar_alunos()
    idx = IntPrompt.ask("  Selecione o aluno para editar", default=1) - 1
    if not (0 <= idx < len(alunos)):
        console.print("  ❌ [red]Aluno inválido[/red]")
        return
    aluno = alunos[idx]
    console.print(Panel(f"✏️ [bold]Editar: {aluno.nome} ({aluno.matricula})[/bold]", border_style="yellow"))
    novo_nome = Prompt.ask("  Nome", default=aluno.nome)
    novo_email = Prompt.ask("  Email", default=aluno.email)
    try:
        GerenciadorCursos.editar_aluno(aluno.matricula, novo_nome, novo_email)
        console.print(f"  ✅ [green]Aluno atualizado com sucesso![/green]")
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")

def excluir_aluno():
    alunos = GerenciadorCursos.listar_alunos()
    cursos = GerenciadorCursos._cursos
    if not alunos:
        console.print("  ⚠️ [yellow]Nenhum aluno cadastrado.[/yellow]")
        return
    listar_alunos()
    idx = IntPrompt.ask("  Selecione o aluno para excluir", default=1) - 1
    if not (0 <= idx < len(alunos)):
        console.print("  ❌ [red]Aluno inválido[/red]")
        return
    aluno = alunos[idx]
    matriculas_ativas = [c for c in cursos if aluno in c.alunos]
    if matriculas_ativas:
        console.print(f"  ⚠️ [yellow]Aluno está matriculado em {len(matriculas_ativas)} curso(s):[/yellow]")
        for c in matriculas_ativas:
            console.print(f"     - {c.codigo}: {c.nome}")
        if not Confirm.ask("  Deseja excluir mesmo assim? (será desmatriculado automaticamente)"):
            console.print("  ⚪ [dim]Operação cancelada.[/dim]")
            return
        for curso in matriculas_ativas:
            curso.desmatricular(aluno)
        console.print("  📝 [dim]Aluno desmatriculado dos cursos automaticamente.[/dim]")
    if Confirm.ask(f"  Confirmar exclusão de [red]{aluno.nome}[/red] ({aluno.matricula})?"):
        GerenciadorCursos.excluir_aluno(aluno.matricula)
        console.print(f"  ✅ [green]Aluno excluído com sucesso![/green]")
    else:
        console.print("  ⚪ [dim]Operação cancelada.[/dim]")

def gerenciar_alunos():
    """Loop principal do menu de alunos."""
    while True:
        from main import limpar_tela
        limpar_tela()
        alunos = GerenciadorCursos.listar_alunos()
        sub_opcao = menu_alunos(alunos)
        
        if sub_opcao == 1:
            criar_aluno()
        elif sub_opcao == 2:
            listar_alunos()
        elif sub_opcao == 3:
            editar_aluno()
        elif sub_opcao == 4:
            excluir_aluno()
        elif sub_opcao == 5:
            break
        voltar_ao_menu()