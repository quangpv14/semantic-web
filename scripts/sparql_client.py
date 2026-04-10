
import requests
import json
from sparql_queries import QUERIES

class SparqlClient:
    def __init__(self, base_url="http://localhost:3030", dataset="football"):
        self.base_url = base_url.rstrip('/')
        self.dataset = dataset
        self.endpoint = f"{self.base_url}/{dataset}/sparql"

    def execute_query(self, query, format_type="json"):
        """
        Execute a SPARQL query against the endpoint
        """
        headers = {
            'Accept': 'application/sparql-results+json' if format_type == "json" else 'text/csv',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'query': query
        }

        try:
            response = requests.post(self.endpoint, headers=headers, data=data)
            response.raise_for_status()

            if format_type == "json":
                return response.json()
            else:
                return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error executing query: {e}")
            return None

    def print_results(self, results, limit=10):
        """
        Print query results in a readable format
        """
        if not results or 'results' not in results:
            print("No results or error in query execution")
            return

        bindings = results['results']['bindings']
        if not bindings:
            print("No results found")
            return

        # Get column headers
        if bindings:
            headers = list(bindings[0].keys())
            print(" | ".join(f"{h:<20}" for h in headers))
            print("-" * (len(headers) * 22))

            # Print rows
            for i, binding in enumerate(bindings[:limit]):
                row = []
                for header in headers:
                    value = binding.get(header, {}).get('value', '')
                    # Truncate long values
                    if len(str(value)) > 20:
                        value = str(value)[:17] + "..."
                    row.append(f"{value:<20}")
                print(" | ".join(row))

            if len(bindings) > limit:
                print(f"\n... and {len(bindings) - limit} more results")

    def run_predefined_query(self, query_name):
        """
        Run a predefined query from the QUERIES dictionary
        """
        if query_name not in QUERIES:
            print(f"Query '{query_name}' not found. Available queries:")
            for q in QUERIES.keys():
                print(f"  - {q}")
            return

        print(f"\nExecuting query: {query_name}")
        print("=" * 50)

        query = QUERIES[query_name]
        results = self.execute_query(query)

        if results:
            self.print_results(results)
        else:
            print("Query execution failed")

    def interactive_mode(self):
        """
        Start interactive mode for querying
        """
        print("SPARQL Client for Football Data")
        print(f"Endpoint: {self.endpoint}")
        print("Type 'help' for available commands, 'quit' to exit")
        print()

        while True:
            try:
                cmd = input("sparql> ").strip()

                if cmd.lower() in ['quit', 'exit', 'q']:
                    break
                elif cmd.lower() == 'help':
                    self.show_help()
                elif cmd.lower() == 'list':
                    print("Available predefined queries:")
                    for q in sorted(QUERIES.keys()):
                        print(f"  - {q}")
                elif cmd.startswith('run '):
                    query_name = cmd[4:].strip()
                    self.run_predefined_query(query_name)
                elif cmd.startswith('query '):
                    # Allow direct query input
                    query = cmd[6:].strip()
                    if query:
                        results = self.execute_query(query)
                        if results:
                            self.print_results(results)
                    else:
                        print("Please provide a query after 'query '")
                else:
                    print("Unknown command. Type 'help' for assistance.")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

    def show_help(self):
        """
        Show help information
        """
        print("""
Available commands:
  help          - Show this help message
  list          - List all predefined queries
  run <query>   - Run a predefined query (e.g., 'run all_players')
  query <sparql>- Execute a custom SPARQL query
  quit          - Exit the client

Predefined queries:
  all_players        - Players with nationality, team, goals, assists (top scorers)
  matches            - Matches with teams, score, date, referee, stadium
  referees           - Referees with age, level, matches officiated, stadiums
  player_stats_join  - Players joined with their statistics
  match_referees_join- Matches with teams, score, date, referee, stadium capacity

Examples:
  run all_players
  run matches
  run referees
  query SELECT * WHERE { ?s ?p ?o } LIMIT 10
        """)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='SPARQL Client for Football RDF Data')
    parser.add_argument('--dataset', default='football', help='Dataset name (default: football)')
    parser.add_argument('--port', type=int, default=3030, help='Fuseki port (default: 3030)')
    parser.add_argument('--query', help='Run a specific predefined query and exit')
    parser.add_argument('--custom-query', help='Run a custom SPARQL query and exit')

    args = parser.parse_args()

    client = SparqlClient(f"http://localhost:{args.port}", args.dataset)

    if args.query:
        client.run_predefined_query(args.query)
    elif args.custom_query:
        results = client.execute_query(args.custom_query)
        if results:
            client.print_results(results)
    else:
        client.interactive_mode()

if __name__ == "__main__":
    main()