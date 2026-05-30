<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        api: __DIR__ . '/../routes/api.php',
        commands: __DIR__ . '/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware): void {
        // Add authentication, rate limiting, or CORS middleware here as the app grows.
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        // Centralized exception reporting and rendering belongs here.
    })
    ->create();
