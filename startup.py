"""
Minimal startup script to further improve performance.
Only imports essential modules at startup.
"""
def run_app():
    """Deferred app loading for fastest startup"""
    # Essential imports only
    from multiprocessing import freeze_support
    freeze_support()
    
    # Show early loading message
    print("Starting Berichtsheft Generator...")
    
    # Now load the heavy modules
    from src.main import main
    main()

if __name__ in {"__main__", "__mp_main__"}:
    run_app()
