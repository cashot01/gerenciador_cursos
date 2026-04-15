from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from services.gerenciador import GerenciadorCursos
from views.professor_view import gerenciar_professores
from views.aluno_view import gerenciar_alunos
from views.curso_view import gerenciar_cursos, matricular_aluno, desmatricular_aluno, adicionar_nota, listar_cursos

console = Console()

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def limpar_tela():
    console.print("\n" * 2)

def exibir_cabecalho():
    console.print(Panel.fit(
        "🎓 [bold cyan]Sistema de Gerenciamento de Cursos[/bold cyan]\n"
        "[dim]Python POO + Rich CLI + JSON Persistence + MVC Architecture[/dim]",
        border_style="cyan",
        padding=(1, 2)
    ))

def voltar_ao_menu():
    Prompt.ask("\n[dim]Pressione Enter para continuar[/dim]")

# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def menu_principal() -> int:
    console.print("\n[bold yellow]📋 Menu Principal:[/bold yellow]")
    opcoes = [
        "1. 👨‍🏫 Gerenciar Professores (CRUD)",
        "2. 👨‍🎓 Gerenciar Alunos (CRUD)",
        "3. 📚 Gerenciar Cursos (CRUD)",
        "4. 📝 Matricular Aluno em Curso",
        "5. ❌ Desmatricular Aluno",
        "6. 📊 Adicionar Nota a Aluno",
        "7. 🔍 Listar Todos os Cursos",
        "8. 📈 Gerar Relatório de Turmas",
        "9. 📤 Exportar Relatório para CSV",
        "10. 💾 Salvar Dados Manualmente",
        "11. 🚪 Sair (Salva automaticamente)"
    ]
    for op in opcoes:
        console.print(f"  • {op}")
    return IntPrompt.ask("\n[bold green]Escolha uma opção[/bold green]", default=11)

# ============================================================================
# OPERAÇÕES GLOBAIS
# ============================================================================

def exportar_csv():
    """Exportar relatório para CSV."""
    from views.curso_view import console as view_console
    cursos = GerenciadorCursos._cursos
    if not cursos:
        view_console.print("  ⚠️ [yellow]Nenhum curso cadastrado para exportar.[/yellow]")
        return
    view_console.print(Panel("📤 [bold]Exportar Relatório para CSV[/bold]", border_style="green"))
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=view_console,
        transient=True
    ) as progress:
        task = progress.add_task("Exportando dados...", total=None)
        try:
            caminho = GerenciadorCursos.exportar_relatorio_csv()
            progress.update(task, completed=True)
            total_alunos = sum(len(c.alunos) for c in cursos)
            total_cursos = len(cursos)
            view_console.print(Panel(
                f"[bold green]✅ Exportação concluída com sucesso![/bold green]\n\n"
                f"📁 Arquivo: [cyan]{caminho}[/cyan]\n"
                f"📊 Cursos exportados: [bold]{total_cursos}[/bold]\n"
                f"👨‍🎓 Total de matrículas: [bold]{total_alunos}[/bold]\n\n"
                f"[dim]Abra o arquivo no Excel, Google Sheets ou LibreOffice Calc.[/dim]",
                border_style="green",
                padding=(1, 2)
            ))
        except ValueError as e:
            view_console.print(f"  ❌ [red]Erro: {e}[/red]")
        except Exception as e:
            view_console.print(f"  ❌ [red]Erro inesperado: {e}[/red]")

def gerar_relatorio():
    """Gerar relatório de turmas."""
    from views.curso_view import console as view_console
    view_console.print(Panel("📈 [bold]Relatório de Turmas[/bold]", border_style="magenta"))
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=view_console,
        transient=True
    ) as progress:
        progress.add_task("Gerando relatório...", total=None)
        relatorio = GerenciadorCursos.gerar_relatorio_turmas()
    view_console.print(Markdown(relatorio))

# ============================================================================
# MAIN
# ============================================================================

def main():
    # 1. Carregar dados existentes
    if GerenciadorCursos.carregar_dados():
        console.print("📂 [green]Dados carregados com sucesso do arquivo JSON![/green]")
    
    while True:
        limpar_tela()
        exibir_cabecalho()
        opcao = menu_principal()
        
        if opcao == 1:
            gerenciar_professores()
        elif opcao == 2:
            gerenciar_alunos()
        elif opcao == 3:
            gerenciar_cursos()
        elif opcao == 4:
            matricular_aluno()
            voltar_ao_menu()
        elif opcao == 5:
            desmatricular_aluno()
            voltar_ao_menu()
        elif opcao == 6:
            adicionar_nota()
            voltar_ao_menu()
        elif opcao == 7:
            listar_cursos()
            voltar_ao_menu()
        elif opcao == 8:
            gerar_relatorio()
            voltar_ao_menu()
        elif opcao == 9:
            exportar_csv()
            voltar_ao_menu()
        elif opcao == 10:
            caminho = GerenciadorCursos.salvar_dados()
            console.print(f"💾 [green]Dados salvos em: {caminho}[/green]")
            voltar_ao_menu()
        elif opcao == 11:
            caminho = GerenciadorCursos.salvar_dados()
            console.print(Panel(f"\n[bold green]👋 Dados salvos em: {caminho}\nObrigado por usar o Sistema de Cursos![/bold green]\n", border_style="green"))
            break
        else:
            console.print("  ❌ [red]Opção inválida. Tente novamente.[/red]")
            voltar_ao_menu()

if __name__ == "__main__":
    main()