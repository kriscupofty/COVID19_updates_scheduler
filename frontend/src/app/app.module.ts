import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { EmptyComponent } from './empty/empty.component';

@NgModule({
  declarations: [
    AppComponent,
    PageNotFoundComponent,
    EmptyComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ], 
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
