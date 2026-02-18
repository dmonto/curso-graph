def generate_import_report(results, output_file="import_report.json"):
    """Genera reporte de importación."""
    
    import json
    from datetime import datetime
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": results['success'] + results['failed'],
            "successful": results['success'],
            "failed": results['failed'],
            "success_rate": f"{100 * results['success'] / (results['success'] + results['failed']):.1f}%"
        },
        "errors": results.get('errors', [])
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== REPORTE ===")
    print(f"Total: {report['summary']['total']}")
    print(f"Éxito: {report['summary']['successful']}")
    print(f"Fallido: {report['summary']['failed']}")
    print(f"Tasa: {report['summary']['success_rate']}")
    
    if report['errors']:
        print(f"\nErrores ({len(report['errors'])}):")
        for error in report['errors'][:10]:
            print(f"  - {error}")
        if len(report['errors']) > 10:
            print(f"  ... y {len(report['errors']) - 10} más")
    
    return report

# USO
if __name__ == "__main__":
    report = generate_import_report(results)