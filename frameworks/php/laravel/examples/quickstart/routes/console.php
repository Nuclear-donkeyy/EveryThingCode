<?php

use Illuminate\Support\Facades\Artisan;

Artisan::command('tasks:about', function (): void {
    $this->info('Laravel quickstart exposes GET/POST /api/tasks with a file-backed repository.');
})->purpose('Describe the quickstart task API');
