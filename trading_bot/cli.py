import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt, Confirm
from dotenv import load_dotenv
import os

from bot.client import BinanceFuturesClient
from bot.orders import place_order
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

@app.command()
def order(
    symbol: str = typer.Option(None, help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(None, help="Trade side: BUY or SELL"),
    order_type: str = typer.Option(None, "--type", help="Order type: MARKET, LIMIT, STOP_MARKET"),
    quantity: float = typer.Option(None, help="Quantity to trade"),
    price: float = typer.Option(None, help="Price for LIMIT orders"),
    stop_price: float = typer.Option(None, help="Stop price for STOP_MARKET orders"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Use interactive prompts")
):
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        console.print("[bold red]Error: BINANCE_API_KEY or BINANCE_API_SECRET not found in .env file[/bold red]")
        console.print("Please copy .env.example to .env and fill in your testnet credentials.")
        raise typer.Exit(1)
        
    client = BinanceFuturesClient(api_key, api_secret)
    
    if interactive:
        symbol = Prompt.ask("Enter symbol", default="BTCUSDT").upper()
        side = Prompt.ask("Enter side", choices=["BUY", "SELL"])
        order_type = Prompt.ask("Enter order type", choices=["MARKET", "LIMIT", "STOP_MARKET"])
        quantity = FloatPrompt.ask("Enter quantity")
        if order_type == "LIMIT":
            price = FloatPrompt.ask("Enter price")
        elif order_type == "STOP_MARKET":
            stop_price = FloatPrompt.ask("Enter stop price")
    else:
        if not all([symbol, side, order_type, quantity]):
            console.print("[bold red]Missing required arguments! Use --help to see required options or use --interactive.[/bold red]")
            raise typer.Exit(1)
            
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()

    try:
        validate_symbol(symbol)
        validate_side(side)
        validate_order_type(order_type)
        validate_quantity(quantity)
        
        # Display order request summary
        summary = Table(title="Order Request Summary", show_header=True, header_style="bold magenta")
        summary.add_column("Field")
        summary.add_column("Value")
        summary.add_row("Symbol", symbol)
        summary.add_row("Side", side)
        summary.add_row("Type", order_type)
        summary.add_row("Quantity", str(quantity))
        if price is not None:
            summary.add_row("Price", str(price))
        if stop_price is not None:
            summary.add_row("Stop Price", str(stop_price))
            
        console.print(Panel(summary, expand=False))
        
        if not Confirm.ask("Execute this order on Testnet?"):
            console.print("[yellow]Order cancelled by user.[/yellow]")
            raise typer.Exit(0)
            
        with console.status("[bold green]Placing order on Binance Futures Testnet...[/bold green]"):
            response = place_order(client, symbol, side, order_type, quantity, price, stop_price)
            
        # Display order response details
        res_table = Table(title="Order Response Details", show_header=True, header_style="bold cyan")
        res_table.add_column("Field")
        res_table.add_column("Value")
        
        res_table.add_row("Order ID", str(response.get("orderId", "N/A")))
        res_table.add_row("Status", str(response.get("status", "N/A")))
        res_table.add_row("Executed Qty", str(response.get("executedQty", "N/A")))
        res_table.add_row("Avg Price", str(response.get("avgPrice", "0.0")))
        res_table.add_row("Type", str(response.get("type", order_type)))
        
        console.print(Panel(res_table, expand=False))
        console.print("[bold green]✅ Order successful![/bold green]")

    except Exception as e:
        console.print(f"\n[bold red]❌ Order failed:[/bold red] {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
