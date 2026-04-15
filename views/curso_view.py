from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import IntPrompt, Prompt, FloatPrompt, Confirm

from models.curso import Curso
from models.aluno import Aluno
from services.gerenciador import GerenciadorCursos

console = Console()

def voltar_ao_menu():
    Prompt.ask("\n[dim]Pressione Enter para continuar[/dim]")

def menu_cursos() -> int:
    console.print(Panel("[bold magenta]📚 Gerenciar Cursos[/bold magenta]", border_style="magenta"))
    opcoes = [
        "1. ➕ Cadastrar Novo Curso",
        "2. 👁️ Listar Todos os Cursos",
        "3. ✏️ Editar Curso",
        "4. 🗑️ Excluir Curso",
        "5. 🔙 Voltar ao Menu Principal"
    ]
    for op in opcoes:
        console.print(f"  • {op}")
    return IntPrompt.ask("\n[bold green]Escolha uma opção[/bold green]", default=5)

def criar_curso() -> Curso | None:
    professores = GerenciadorCursos.listar_professores()
    if not professores:
        console.print("  ⚠️ [yellow]Nenhum professor cadastrado. Cadastre um primeiro![/yellow]")
        return None
    console.print(Panel("➕ [bold]Novo Curso[/bold]", border_style="magenta"))
    table = Table(title="Professores Disponíveis", show_lines=True)
    table.add_column("#", style="dim")
    table.add_column("Nome")
    table.add_column("Especialidade")
    for i, p in enumerate(professores, 1):
        table.add_row(str(i), p.nome, p.especialidade)
    console.print(table)
    idx = IntPrompt.ask("  Selecione o professor (número)", default=1) - 1
    if not (0 <= idx < len(professores)):
        console.print("  ❌ [red]Professor inválido[/red]")
        return None
    codigo = Prompt.ask("  Código do curso (ex: PY101)").upper()
    nome = Prompt.ask("  Nome do curso")
    carga = IntPrompt.ask("  Carga horária (horas)", default=40)
    curso = Curso(codigo, nome, carga, professores[idx])
    GerenciadorCursos.adicionar_curso(curso)
    console.print(f"  ✅ [green]Curso '{curso.nome}' cadastrado com sucesso![/green]")
    return curso

def listar_cursos():
    console.print(Panel("👁️ [bold]Cursos Cadastrados[/bold]", border_style="magenta"))
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  📭 [dim]Nenhum curso cadastrado ainda.[/dim]")
        return
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Código", style="cyan")
    table.add_column("Curso")
    table.add_column("Carga")
    table.add_column("Professor")
    table.add_column("Alunos", justify="right")
    for i, curso in enumerate(cursos, 1):
        table.add_row(
            str(i),
            curso.codigo,
            curso.nome,
            f"{curso.carga_horaria}h",
            curso.professor.nome,
            str(len(curso.alunos))
        )
    console.print(table)

def editar_curso():
    cursos = GerenciadorCursos._cursos
    professores = GerenciadorCursos.listar_professores()
    if not cursos:
        console.print("  ⚠️ [yellow]Nenhum curso cadastrado.[/yellow]")
        return
    listar_cursos()
    idx = IntPrompt.ask("  Selecione o curso para editar", default=1) - 1
    if not (0 <= idx < len(cursos)):
        console.print("  ❌ [red]Curso inválido[/red]")
        return
    curso = cursos[idx]
    console.print(Panel(f"✏️ [bold]Editar: {curso.nome} ({curso.codigo})[/bold]", border_style="yellow"))
    console.print("\n[bold]Professores disponíveis:[/bold]")
    table = Table(show_lines=True)
    table.add_column("#", style="dim")
    table.add_column("Nome")
    table.add_column("Especialidade")
    for i, p in enumerate(professores, 1):
        table.add_row(str(i), p.nome, p.especialidade)
    console.print(table)
    idx_prof = IntPrompt.ask("  Selecione o professor", default=1) - 1
    if not (0 <= idx_prof < len(professores)):
        console.print("  ❌ [red]Professor inválido[/red]")
        return
    novo_nome = Prompt.ask("  Nome do curso", default=curso.nome)
    nova_carga = IntPrompt.ask("  Carga horária (horas)", default=curso.carga_horaria)
    curso.nome = novo_nome
    curso.carga_horaria = nova_carga
    curso.professor = professores[idx_prof]
    console.print(f"  ✅ [green]Curso atualizado com sucesso![/green]")

def excluir_curso():
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  ⚠️ [yellow]Nenhum curso cadastrado.[/yellow]")
        return
    listar_cursos()
    idx = IntPrompt.ask("  Selecione o curso para excluir", default=1) - 1
    if not (0 <= idx < len(cursos)):
        console.print("  ❌ [red]Curso inválido[/red]")
        return
    curso = cursos[idx]
    if curso.alunos:
        console.print(f"  ⚠️ [yellow]Curso possui {len(curso.alunos)} aluno(s) matriculado(s).[/yellow]")
        if not Confirm.ask("  Deseja excluir mesmo assim? (alunos serão desmatriculados)"):
            console.print("  ⚪ [dim]Operação cancelada.[/dim]")
            return
        curso.alunos.clear()
        console.print("  📝 [dim]Todos os alunos foram desmatriculados automaticamente.[/dim]")
    if Confirm.ask(f"  Confirmar exclusão de [red]{curso.nome}[/red] ({curso.codigo})?"):
        GerenciadorCursos._cursos.remove(curso)
        console.print(f"  ✅ [green]Curso excluído com sucesso![/green]")
    else:
        console.print("  ⚪ [dim]Operação cancelada.[/dim]")

def matricular_aluno():
    """Matricular aluno em curso."""
    cursos = GerenciadorCursos._cursos
    alunos = GerenciadorCursos.listar_alunos()
    if not cursos or not alunos:
        console.print("  ⚠️ [yellow]É necessário ter cursos e alunos cadastrados.[/yellow]")
        return
    console.print(Panel("📝 [bold]Matricular Aluno[/bold]", border_style="cyan"))
    console.print("\n[bold]Cursos disponíveis:[/bold]")
    for i, c in enumerate(cursos, 1):
        console.print(f"  {i}. {c.codigo} - {c.nome}")
    idx_curso = IntPrompt.ask("  Selecione o curso", default=1) - 1
    console.print("\n[bold]Alunos disponíveis:[/bold]")
    for i, a in enumerate(alunos, 1):
        console.print(f"  {i}. {a.matricula} - {a.nome}")
    idx_aluno = IntPrompt.ask("  Selecione o aluno", default=1) - 1
    try:
        cursos[idx_curso].matricular(alunos[idx_aluno])
        console.print(f"  ✅ [green]{alunos[idx_aluno].nome} matriculado em {cursos[idx_curso].nome}![/green]")
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")

def desmatricular_aluno():
    """Desmatricular aluno de curso."""
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  ⚠️ [yellow]Nenhum curso disponível.[/yellow]")
        return
    console.print(Panel("❌ [bold]Desmatricular Aluno[/bold]", border_style="red"))
    cursos_com_alunos = [c for c in cursos if c.alunos]
    if not cursos_com_alunos:
        console.print("  ⚠️ [yellow]Nenhum curso com alunos matriculados.[/yellow]")
        return
    console.print("\n[bold]Cursos com matrículas:[/bold]")
    for i, c in enumerate(cursos_com_alunos, 1):
        console.print(f"  {i}. [cyan]{c.codigo}[/cyan] - {c.nome} ({len(c.alunos)} alunos)")
    idx_curso = IntPrompt.ask("  Selecione o curso", default=1) - 1
    if not (0 <= idx_curso < len(cursos_com_alunos)):
        console.print("  ❌ [red]Curso inválido[/red]")
        return
    curso = cursos_com_alunos[idx_curso]
    console.print(f"\n[bold]Alunos matriculados em [cyan]{curso.nome}[/cyan]:[/bold]")
    table = Table(show_header=True, header_style="bold red", show_lines=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Matrícula", style="cyan")
    table.add_column("Nome")
    table.add_column("Média", justify="right")
    for i, aluno in enumerate(curso.alunos, 1):
        table.add_row(str(i), aluno.matricula, aluno.nome, f"{aluno.calcular_media():.1f}")
    console.print(table)
    idx_aluno = IntPrompt.ask("  Selecione o aluno para desmatricular", default=1) - 1
    if not (0 <= idx_aluno < len(curso.alunos)):
        console.print("  ❌ [red]Aluno inválido[/red]")
        return
    aluno_selecionado = curso.alunos[idx_aluno]
    console.print(Panel(
        f"[bold]Confirmação[/bold]\n"
        f"Desmatricular [yellow]{aluno_selecionado.nome}[/yellow] ([cyan]{aluno_selecionado.matricula}[/cyan])\n"
        f"do curso [cyan]{curso.nome}[/cyan]?",
        border_style="yellow", padding=(1, 2)
    ))
    confirm = Prompt.ask("  Digite [bold]SIM[/bold] para confirmar", default="não").strip().upper()
    if confirm == "SIM":
        try:
            curso.desmatricular(aluno_selecionado)
            console.print(f"  ✅ [green]{aluno_selecionado.nome} desmatriculado com sucesso![/green]")
        except ValueError as e:
            console.print(f"  ❌ [red]Erro: {e}[/red]")
    else:
        console.print("  ⚪ [dim]Operação cancelada.[/dim]")

def adicionar_nota():
    """Adicionar nota a aluno matriculado."""
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  ⚠️ [yellow]Nenhum curso disponível.[/yellow]")
        return
    console.print(Panel("📊 [bold]Adicionar Nota[/bold]", border_style="yellow"))
    cursos_com_alunos = [c for c in cursos if c.alunos]
    if not cursos_com_alunos:
        console.print("  ⚠️ [yellow]Nenhum curso com alunos matriculados.[/yellow]")
        return
    console.print("\n[bold]Cursos com alunos:[/bold]")
    for i, c in enumerate(cursos_com_alunos, 1):
        console.print(f"  {i}. {c.codigo} - {c.nome} ({len(c.alunos)} alunos)")
    idx = IntPrompt.ask("  Selecione o curso", default=1) - 1
    curso = cursos_com_alunos[idx]
    console.print("\n[bold]Alunos matriculados:[/bold]")
    for i, a in enumerate(curso.alunos, 1):
        console.print(f"  {i}. {a.matricula} - {a.nome} | Média atual: {a.calcular_media():.1f}")
    idx_aluno = IntPrompt.ask("  Selecione o aluno", default=1) - 1
    aluno = curso.alunos[idx_aluno]
    nota = FloatPrompt.ask("  Digite a nota (0.0 a 10.0)")
    try:
        aluno.adicionar_nota(nota)
        console.print(f"  ✅ [green]Nota {nota} adicionada! Nova média: {aluno.calcular_media():.1f}[/green]")
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")

def gerenciar_cursos():
    """Loop principal do menu de cursos."""
    while True:
        from main import limpar_tela
        limpar_tela()
        sub_opcao = menu_cursos()
        
        if sub_opcao == 1:
            criar_curso()
        elif sub_opcao == 2:
            listar_cursos()
        elif sub_opcao == 3:
            editar_curso()
        elif sub_opcao == 4:
            excluir_curso()
        elif sub_opcao == 5:
            break
        voltar_ao_menu()